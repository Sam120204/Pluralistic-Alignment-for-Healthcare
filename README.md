# Pluralistic-Alignment-for-Healthcare

This repository contains code and scripts for our ACL 2025 submission:
**"Pluralistic Alignment for Healthcare: A Role-Driven Framework"**.

We propose **ETHOSAGENTS**, a lightweight, generalizable framework for pluralistic alignment in healthcare, leveraging structured persona simulation to generate ethically diverse responses across three alignment modes:

* **Overton**: freeform multi-perspective reasoning,
* **Steerable**: conditioned generation from chosen personas,
* **Distributional**: population-aligned distribution modeling.

## Paper

You can find our paper [here (ACL submission)](./7854_Pluralistic_Alignment_for.pdf). ETHOSAGENTS outperforms prior baselines (e.g., Modular Pluralism, MoE) across all three alignment tasks on the [VITAL dataset](https://github.com/anudeex/VITAL/tree/main/dataset).

## File Structure

| Script                                                | Description                                                        |
| ----------------------------------------------------- | ------------------------------------------------------------------ |
| `generate_distributional_comments_moral_scenarios.py` | Distributional generation for moral dilemmas                       |
| `generate_distributional_comments_poll_questions.py`  | Distributional generation for public opinion poll questions        |
| `generate_overton_comments.py`                        | Overton-style comment generation (multi-perspective summarization) |
| `generate_steerable_comments_generate.py`             | Steerable generation conditioned on persona                        |
| `generate_steerable_comments_probability.py`          | Steerable generation with soft persona selection                   |

Each script supports multiprocessing, resume-from-checkpoint, and dynamic persona conditioning.

## Dataset

We use the [VITAL benchmark](https://github.com/anudeex/VITAL/tree/main/dataset), a pluralism-focused dataset designed for health-related moral alignment. It covers:

* Overton (n=1,649)
* Steerable (n=15,340)
* Distributional (n=1,857)

## Related Tools

For distributional alignment and comment merging, we build on ideas from [Modular Pluralism](https://github.com/BunsenFeng/modular_pluralism/tree/main). Our approach differs by avoiding fine-tuned submodels, instead generating diverse perspectives on-the-fly.

## Citation

```bibtex
@inproceedings{ethosagents2025,
  title={Pluralistic Alignment for Healthcare: A Role-Driven Framework},
  author={Anonymous},
  booktitle={ACL},
  year={2025}
}
```

## Contact

For questions, reach out via GitHub Issues or connect with the authors after acceptance.
