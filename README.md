# s26-p2-submission-backend

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](../../actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## What the Project Does

**s26-p2-submission-backend** is a submission packaging toolkit for CMU 11-785/11-685 HWP2 Deep Learning assignments. It provides an automated way to validate and package student submissions for project part 2 (P2), including Kaggle competitions and Weights & Biases (W&B) experiment tracking.

## How to Get Started

### Prerequisites

- Python 3.8+
- [Kaggle API](https://github.com/Kaggle/kaggle-api) credentials (for Kaggle validation)
- [Weights & Biases](https://wandb.ai/) account (for experiment tracking)

### Installation

Clone the repository and install dependencies:

```bash
git clone <this-repo-url>
cd s26-p2-submission-backend
pip install -r requirements.txt  # if provided, else install kaggle, wandb
```

### Usage

#### 1. Simulate Autolab Grading

```bash
make simulate
```

This will create a dummy submission and run the autograder simulation locally.

#### 2. Package Your Submission

Edit and use the scripts in `submission/` to generate required files:

- `main.py`: Main entry for packaging and validation
- `backend_config.py`, `submission_config.py`: Define experiment and submission configs
- `model_metadata.py`: Build model metadata for auditing
- `wandb_export.py`: Export top W&B runs
- `kaggle_validate.py`: Validate Kaggle submissions

Example (from project root):

```bash
python submission/main.py
```

#### 3. Upload to Autolab

After simulation and packaging, upload the generated `autograde-Makefile` and `autograde.tar` to Autolab as instructed.

### Configuration

Assignment-specific configs are in `submission/configs/` (e.g., `hw1p2.json`). Edit or extend as needed for your assignment.

## Where to Get Help

- Assignment Piazza/Ed forum
- Course staff office hours
- [Kaggle API docs](https://github.com/Kaggle/kaggle-api)
- [Weights & Biases docs](https://docs.wandb.ai/)

## Maintainers and Contributions

- Maintained by the CMU 11-785/11-685 course staff.
- For contributions, see [CONTRIBUTING.md](CONTRIBUTING.md) (if available) or contact the maintainers.

---

_This project is for educational use in CMU 11-785/11-685. For license details, see [LICENSE](LICENSE)._
