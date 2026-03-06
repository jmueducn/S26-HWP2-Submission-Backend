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
├── common.ipynb               # Common notebook cells to include in student notebooks
├── simulate_autolab.py        # Local autograder simulator for TAs
├── Makefile                   # TA Makefile for autograder simulation and packaging
└── README.md                  # This file

```

---

## Common TA Tasks

### Updating for a New Semester

Follow the steps below to prepare the homework infrastructure for a new semester.

1. **Update configuration**

   - Modify `submission/configs/hwXp2.json` with:

     - The new competition name(s)
     - Updated parameter limits and constraints

   - Replace `X` with the appropriate homework number.
   - For more details, refer to the **Configuration File Instructions** section below.

2. **Verify the submission pipeline**

   - Run:

     ```bash
     make simulate
     ```

   - Confirm that the submission process completes successfully end-to-end.

3. **Generate Autolab grading artifacts**

   - Create the Autolab assignment files by running:

     ```bash
     make autolab
     ```

   - This should generate:

     - `autograde-Makefile`
     - `autograde.tar`

4. **Create the Autolab assignment**
   - Create a new assignment in Autolab and upload the generated `autograde-Makefile` and `autograde.tar`. Please follow the steps below.

   1. Create a new assignment in Autolab:

      Autolab → Install Assessment → **Create from scratch** → **Create New Assessment**

      Set:
      - **Display name**
      - **Category name**

      Then click **Create Assessment**.

   2. Configure the Autograder:

      Go to:

      **Edit assessment → Basic → Modules Used**

      Click the **+** next to **Autograder**.

      In **Autograder Settings**, set:

      - **VM Image:** `11785_f24.img`

      Upload the files generated in Step 3:

      - `autograde-Makefile`
      - `autograde.tar`

      Then click **Save Settings**.

   3. Configure Handin settings:

      Under **Handin**, set:

      - **Deadlines**
      - **Max submission size**

   4. Add the validation problem:

      Go to **Problems → Add Problem**

      Set:

      - **Name:** `validate-zip`
      - **Max score:** `100`

      Then click **Save Problem**.

5. **Update the homework notebook**

   - Copy the required common cells from `common.ipynb` into the homework notebook.
   - Ensure all submission-related cells are present and ordered correctly.

6. **End-to-end testing (student perspective)**

   - Generate a submission directly from the notebook.
   - Upload the submission to Autolab.
   - Verify that:

     - The submission is accepted
     - Autograding runs successfully
     - Scores and feedback match expectations

7. **Update student-facing documentation**

   - Revise the homework instructions to clearly describe:

     - How to generate a submission
     - How to upload to Autolab
     - Any common pitfalls or constraints

### Debugging Student Issues

Most failures fall into:

- Missing API keys
- Incorrect file paths
- Forgotten acknowledgement flag
- No valid Kaggle submissions

Backend error messages are intentionally explicit.

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

Below is a cleaned-up version with clear **instructions** explaining each field, plus a short **editing guide** so future TAs/students know exactly what to change and what _not_ to touch.

---

### Configuration File Instructions

The JSON files in `submission/configs` control submission validation and competition routing for the homework. **Update these values at the start of each semester or when creating a new homework instance.**

#### Key Configuration Variables

```json
{
  "param_limit": 20000000000,
  "main_competition_name": "hw-1-p-2-spring-2026-sandbox-testing",
  "slack_competition_name": "hw-1-p-2-spring-2026-sandbox-testing",
  "submission_zip": "HW1P2_final_submission.zip"
}
```

#### Field Descriptions

- **`param_limit`**

  - Maximum allowed number of model parameters.
  - Submissions exceeding this limit will be rejected during validation.
  - Update only if the assignment explicitly changes model size constraints.
  - **Units:** raw parameter count (not millions or billions).

- **`main_competition_name`**

  - The primary competition identifier used for official submissions.
  - Must exactly match the competition name configured in the backend (e.g., Kaggle).
  - Update this value **every semester** to avoid collisions with past offerings.
  - Used to validate a student's kaggle username and submission history.

- **`slack_competition_name`**

  - The competition used for “slack” submissions.
  - During TA Testing, this may be the same as `main_competition_name`.
  - Update this value **every semester** to avoid collisions with past offerings.
  - Used to validate a student's kaggle username and submission history.

- **`submission_zip`**

  - The expected filename of the final submission archive generated by the notebook.

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

[[TODO: Describe autolab folder contents here: How testing_framework.py and runner.py work, how to register new tests, and how to ensure compatibility with autolab etc.]]

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
