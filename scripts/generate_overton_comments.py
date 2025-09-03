import torch.multiprocessing as mp
import json
import re
import copy
from typing import List, Dict
from tqdm import tqdm
from oai_client import OpenAIClient
import os
from dotenv import load_dotenv

load_dotenv()

def generate_seed_personalities(situation: str, num_groups=6) -> List[str]:
    client = OpenAIClient(model="deepseek-reasoner", api_key=os.getenv("DEEPSEEK_API_KEY"))

    prompt = f"""
Generate {num_groups} contrasting ethical perspectives on: "{situation}

Each perspective must differ clearly in:
- Core values
- Ethical framework
- Key right/duty emphasized
- Emotion
- Stakeholder role

FORMAT EACH PERSPECTIVE EXACTLY LIKE THIS (start each with # symbol):
#Name: Core Value, Ethical Framework, Right/Duty, Emotion, Stakeholder
    """

    response = client.call_oai([
        {"role": "system", "content": "Generate diverse ethical perspectives concisely using the exact requested format."},
        {"role": "user", "content": prompt}
    ], max_new_tokens=450, temperature=1)

    groups = [line.split('#', 1)[1].strip() for line in response.strip().split('\n') if line.startswith('#')]

    if len(groups) < num_groups:
        return generate_seed_personalities(situation, num_groups)

    return groups

def generate_detailed_comment(situation: str, personality: str) -> List[dict[str, str]]:
    client = OpenAIClient(model="Qwen2.5-7B", api_key=os.getenv("qwen_api_key"))

    prompt = f"""
Situation: "{situation}"
Perspective: {personality}

Provide a direct moral comment with 180 words clearly stating:
- 2-3 core moral values involved.
- Specific rights or duties relevant.
- Ethical judgment and reasoning.
- Normative language (e.g., should, must).

Begin immediately without introduction.
"""

    messages = [
        {"role": "system", "content": "Directly analyze moral values, rights, and duties clearly and concisely from given perspective."},
        {"role": "user", "content": prompt}
    ]

    response = client.call_oai(messages, max_new_tokens=200, temperature=1)
    response = re.sub(r'^(As a|From the perspective|Speaking as).*?[:;]', '', response, flags=re.I).strip()

    messages.append({"role": "assistant", "content": response})
    return messages

def generate_comments_for_item(item):
    seeds = generate_seed_personalities(item['situation'])
    comments = []

    for seed in seeds:
        comment = generate_detailed_comment(item['situation'], seed)
        comments.append({"seed": seed, "comment": comment})

    return {
        "id": item['id'],
        "situation": item['situation'],
        "vrd": item.get('vrd', None),
        "explanation": item.get('explanation', None),
        "seed_groups": seeds,
        "comments": comments
    }

def worker(input_queue, output_queue):
    while True:
        item = input_queue.get()
        if item is None:
            break
        try:
            result = generate_comments_for_item(item)
            output_queue.put(result)
        except Exception as e:
            output_queue.put({"id": item['id'], "vrd": item['vrd'], "explanation": item['explanation'],
                              "comments": ["Error occurred"], "seed_groups": []})

if __name__ == "__main__":
    with open('input/vital_overton_valuekaleidoscope.json', 'r') as f:
        all_data = json.load(f)

    existing_results_path = 'comments/vital_overton_comments_deepseek.json'
    try:
        with open(existing_results_path, 'r') as f:
            existing_results = json.load(f)
        processed_ids = {result['id'] for result in existing_results}
    except FileNotFoundError:
        existing_results = []
        processed_ids = set()

    remaining_data = [item for item in all_data if item['id'] not in processed_ids]

    if not remaining_data:
        exit(0)

    input_queue = mp.Queue()
    output_queue = mp.Queue()
    processes = []
    num_workers = 64

    for _ in range(num_workers):
        p = mp.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for item in remaining_data:
        input_queue.put(item)

    for _ in range(num_workers):
        input_queue.put(None)

    new_results = []
    for _ in tqdm(range(len(remaining_data)), desc="Processing remaining items"):
        new_results.append(output_queue.get())

    for p in processes:
        p.join()

    combined_results = existing_results + new_results

    output_path = 'results/comments_deepseek.json'
    with open(output_path, 'w') as f:
        json.dump(combined_results, f, indent=4)
