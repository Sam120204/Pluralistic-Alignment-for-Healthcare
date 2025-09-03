# Pluralistic Alignment for Healthcare: A Role-Driven Framework

This repository supports our research paper titled *Pluralistic Alignment for Healthcare: A Role-Driven Framework*. (In Proceedings of EMNLP 2025 MainConference).

<br />

We introduce a two-stage framework (ETHOSAGENTS):

1. **Perspective Generation**: Automatically generate diverse ethical perspectives using a dedicated persona prompt schema.
2. **Comment Generation**: Each perspective is used to generate a detailed moral comment for a given medical or ethical question.

The framework supports scenarios from three core alignment settings:

* **Overton** (multi-perspective summarization)
* **Steerable** (persona-conditioned generation)
* **Distributional** (population-aligned generation)


<br />

<div align="center">

<img width="800" alt="Pluralistic alignment example" src="https://github.com/user-attachments/assets/6c0f31f1-467b-42ef-b515-2364da754378" />
<p><strong>An illustration of different pluralistic alignment modes for a multi-opinionated health scenario</strong></p>

<br />

<img width="600" alt="Overview of alignment datasets" src="https://github.com/user-attachments/assets/39c2937c-6cec-456a-a2d0-dd664f68d9fa" />
<p><strong>Overview of ETHOSAGENTS</strong></p>

</div>

<br />


## Abstract

As large language models are increasingly deployed in sensitive domains such as healthcare, ensuring their outputs reflect the diverse values and perspectives held across populations is critical. However, existing alignment approaches, including pluralistic paradigms like Modular Pluralism, often fall short in the health domain, where personal, cultural, and situational factors shape pluralism. Motivated by the aforementioned healthcare challenges, we propose a first lightweight, generalizable, pluralistic alignment approach, ETHOSAGENTS, designed to simulate diverse perspectives and values. We empirically show that it advances the pluralistic alignment for all three modes across seven varying-sized open and closed models. Our findings reveal that health-related pluralism demands adaptable and normatively aware approaches, offering insights into how these models can better respect diversity in other high-stakes domains.


## Datasets

We utilize examples and formats based on the [VITAL dataset](https://github.com/anudeex/VITAL/tree/main/dataset). Please refer to the original repository for access to the JSON files and schema.

## Comment Combination Strategy

To aggregate generated comments into a final structured output, we adopt a modular pluralism technique inspired by the implementation in [Modular Pluralism](https://github.com/BunsenFeng/modular_pluralism/tree/main). This allows for filtered and structured integration of diverse responses based on coherence and representation metrics.

## Scripts

* `generate_overton_comments.py`: Generates multi-perspective Overton-style summaries.
* `generate_steerable_comments_generate.py`: Generates steerable comments based on fixed personas.
* `generate_steerable_comments_probability.py`: Generates steerable comments based on probabilistic persona weighting.
* `generate_distributional_comments_moral_scenarios.py`: Generates distributional moral comments for VITAL moral choice scenarios.
* `generate_distributional_comments_poll_questions.py`: Generates distributional comments for Global OpinionQA-style questions.

## Citation

*Citation details will be updated upon publication.*

---

For questions or collaborations, please contact the authors listed in the paper.
