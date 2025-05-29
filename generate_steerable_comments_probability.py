import torch.multiprocessing as mp
import json
import re
from typing import List
from tqdm import tqdm
from oai_client import OpenAIClient
import os
from dotenv import load_dotenv

load_dotenv()

def generate_seed_personalities(question: str, num_groups=6) -> List[str]:
    client = OpenAIClient(model="deepseek-reasoner", api_key=os.getenv("DEEPSEEK_API_KEY"))

    prompt = f"""
Generate {num_groups} contrasting ethical perspectives on: "{question}

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
        print(f"Warning: Generated {len(groups)} groups, retrying.")
        print(response, '\n\n')
        return generate_seed_personalities(question, num_groups)

    return groups

def generate_detailed_comment(input_text: str, personality: str) -> List[dict[str, str]]:
    client = OpenAIClient(model="Qwen2.5-7B", api_key=os.getenv("qwen_api_key"))

    prompt = f"""
Input: "{input_text}"
Perspective: {personality}

Provide a direct moral comment (150-180 words) answering the question in the input. 
Explicitly start your answer with the chosen option (A, B, or C) clearly indicated at the very beginning of your comment, followed by your reasoning:
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
    question = item.get('question', '')
    seeds = generate_seed_personalities(question)
    comments = []

    for seed in seeds:
        comment = generate_detailed_comment(question, seed)
        comments.append({"seed": seed, "comment": comment})

    return {
        "id": item['id'],
        "question": question,
        "options": item.get('options', None),
        "attribute": item.get('attribute', None),
        "gold_distribution": item.get('gold_distribution', None),
        "pred_distribution": item.get('pred_distribution', None),
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
            print(f"Error processing item {item.get('id', 'unknown')}: {e}")
            output_queue.put({"id": item.get('id', 'unknown'), "error": str(e)})

if __name__ == "__main__":
    with open('input/vital_steerable_opinionqa.json', 'r') as f:
        data = json.load(f)

    output_path = 'results/vital_steerable_opinionqa_comments_deepseek_chat.json'

    try:
        with open(output_path, 'r') as f:
            existing_results = json.load(f)
            processed_ids = {result['id'] for result in existing_results}
            print(f"Loaded {len(existing_results)} existing results to resume processing")
    except (FileNotFoundError, json.JSONDecodeError):
        existing_results = []
        processed_ids = set()
        print("Starting fresh processing")

    remaining_data = [item for item in data if item['id'] not in processed_ids]
    print(f"Processing {len(remaining_data)} remaining items out of {len(data)} total")

    if not remaining_data:
        print("No remaining items to process")
        exit(0)

    input_queue = mp.Queue()
    output_queue = mp.Queue()
    processes = []
    num_workers = 64

    def saver_process(output_queue, save_every=10):
        results = existing_results.copy()
        completed = 0
        try:
            while True:
                result = output_queue.get()
                if result is None:
                    break
                results.append(result)
                completed += 1
                if completed % save_every == 0:
                    with open(output_path, 'w') as f:
                        json.dump(results, f, indent=4)
                    print(f"Saved progress: {len(results)} items ({completed} new)")
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=4)
            print(f"Processing complete. Saved {len(results)} total results")
        except Exception as e:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=4)
            print(f"Error in saver process: {e}")
            print(f"Emergency save completed with {len(results)} results")

    for _ in range(num_workers):
        p = mp.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    saver = mp.Process(target=saver_process, args=(output_queue,))
    saver.start()

    for item in remaining_data:
        input_queue.put(item)

    for _ in range(num_workers):
        input_queue.put(None)

    for p in processes:
        p.join()

    output_queue.put(None)
    saver.join()

    print(f"Save to {output_path}")
    print("All processes completed")
