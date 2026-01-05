# HWP2 Submission Backend – TA Documentation

This repository contains the proposed **course-wide submission framework** used to
standardize student submissions for Autolab grading for HWP2's.

It is designed to:

- Enforce submission acknowledgements
- Collect student-written README files
- Validate student Kaggle usernames
- Collect WandB experiment logs
- Package all required artifacts into a single ZIP file for Autolab

This README is intended **for future TAs and instructors** maintaining or
reusing this infrastructure.

---

## Repository Overview

```
.
├── submission            # Core submission logic (TA-maintained)
|  ├── configs            # TA-controlled configuration files
|  │    └── ...json          # Example config files (if any)
|  |
|  ├── __init__.py
|  ├── acknowledgement.py   # Acknowledgement text
|  ├── backend_config.py    # TA-controlled backend configuration
|  ├── kaggle_validate.py   # Kaggle API interaction logic
|  ├── main.py              # Main submission orchestration logic
|  ├── model_metadata.py    # Model metadata generation logic
|  ├── submission_config.py # Student-editable submission configuration
|  └──  wandb_adapter.py    # WandB API interaction logic
|
├── autolab  # Autolab grading files to set up autograder
|  ├── runner.py             # Autolab grader entry point
|  └── testing_framework.py  # Autolab testing framework
|
├── simulate_autolab.py        # Local autograder simulator for TAs
├── Makefile                   # TA Makefile for autograder simulation and packaging
└── README.md                  # This file

```

---

## Folder: `submission`

### Purpose

The folder `submission` contains **all logic** required to:

- Validate submissions
- Export WandB runs
- Query Kaggle for official scores
- Enforce deadlines and Slack-day rules
- Generate the final Autolab ZIP artifact

---

### High-Level Flow

The backend performs the following steps in order:

1. **Acknowledgement Enforcement**

   - Students must explicitly set a global variable `ACKNOWLEDGED = True` in their notebook
   - An `acknowledgement.txt` file is generated and included in the submission ZIP, the content of which is defined in `acknowledgement.py`

2. **README Generation**

   - Saves a student-completed `README.txt` describing:
     - Model architecture
     - Training strategy
     - Augmentations
     - Notebook execution notes

3. **WandB Export**

   - Logs into WandB using the student's API key
   - Pulls the top `N` runs based on a `+created_at` timestamp tiebreaker
   - Serializes run metadata + limited history into a `.pkl` file

4. **Kaggle Score Retrieval**

   - Authenticates using Kaggle API credentials
   - Checks both regular and Slack competitions to see if user has valid submissions
   - Extracts the competitions submitted to and the number of submissions made
   - Saves structured metadata to a `.json` file

5. **Submission Packaging**
   - Validates existence of all required files
   - Flattens paths and zips artifacts into a single submission zip file

---

### Key Configuration (TA-Controlled)

[[TODO: List key configuration variables here, e.g., number of WandB runs to pull, competition names, etc.]]

---

### Student Responsibilities

Students are expected to:

1. Fill out metadata:
   - Final model state
   - Kaggle username
   - WandB project
   - README contents
2. Provide correct file paths for Notebook
3. Explicitly accept the acknowledgement
4. Run the final submission cell

---

## Folder: `autolab`

[[TODO: Describe autolab folder contents here.]]

---

## Common TA Tasks

### Updating for a New Semester

[[TODO: List steps to update for a new semester here eg. updating config files etc.]]

### Debugging Student Issues

Most failures fall into:

- Missing API keys
- Incorrect file paths
- Forgotten acknowledgement flag
- No valid Kaggle submissions

Backend error messages are intentionally explicit.

---

## Recommended Future Improvements

[[TODO: List potential enhancements here.]]

---

## Contact / Ownership

Maintained by:
**Course Staff / TA Team**

If you inherit this codebase:

- Read this README first
- Avoid modifying backend logic mid-semester
- Prefer additive changes over refactors
