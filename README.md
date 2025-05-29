# Pluralistic-Alignment-for-Healthcare

## Pluralistic Alignment for Healthcare: A Role-Driven Framework

This repository supports our research paper titled *Pluralistic Alignment for Healthcare: A Role-Driven Framework*. It explores how AI systems can generate diverse moral commentary in clinical and health-related scenarios by simulating perspectives derived from contrasting stakeholder roles and ethical viewpoints.

## Overview

We introduce a two-stage framework:

1. **Perspective Generation**: Automatically generate diverse ethical perspectives using a dedicated persona prompt schema.
2. **Comment Generation**: Each perspective is used to generate a detailed moral comment for a given medical or ethical question.

The framework supports scenarios from three core alignment settings:

* **Overton** (multi-perspective summarization)
* **Steerable** (persona-conditioned generation)
* **Distributional** (population-aligned generation)

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
