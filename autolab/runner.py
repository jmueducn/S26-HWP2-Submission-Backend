#!/usr/bin/env python3
"""
Autolab Grader Entry Point

This script:
  • Loads student submission
  • Executes categorized tests
  • Applies rubric-based scoring
  • Emits a single JSON object to stdout
"""

import json
import zipfile
import os
import glob
from testing_framework import TestingFramework


###############################################################################
# Rubric (must sum to ≤ 100)
###############################################################################

RUBRIC = {
    "validate-zip": 100.0,
}

###############################################################################
# Configuration
###############################################################################

REQUIRED_FILES = {
    "ACKNOWLEDGEMENT.txt",
    "README.txt",
    "model_metadata.json",
    "wandb_export.pkl",
    "kaggle_metadata.json",
}

ZIP_GLOB = "*.zip"

###############################################################################
# Test Cases
###############################################################################

def test_validate_zip():
    """
    Test to validate the contents of the submitted ZIP file.
    """
    # Find the ZIP file in the current directory
    zip_files = glob.glob(ZIP_GLOB)
    assert len(zip_files) == 1, f"Expected exactly one ZIP file matching '{ZIP_GLOB}', found {len(zip_files)}."

    zip_path = zip_files[0]

    assert os.path.isfile(zip_path), f"ZIP file '{zip_path}' does not exist or is not a file."
    assert zipfile.is_zipfile(zip_path), f"File '{zip_path}' is not a valid ZIP file."

    # Open the ZIP file and check its contents
    with zipfile.ZipFile(zip_path, 'r') as z:
        zip_contents = set(z.namelist())
        missing_files = REQUIRED_FILES - zip_contents
        assert not missing_files, f"Missing required files in ZIP: {', '.join(missing_files)}"

    print(f"Test Passed: Submission ZIP validated successfully: {zip_path}")


###############################################################################
# Grader Logic
###############################################################################

def main() -> None:
    
    # Initialize testing framework
    framework = TestingFramework(
        test_categories={k:[] for k in RUBRIC.keys()}
    )
    
    # Register test cases
    framework.register_test_case(
        category="validate-zip",
        test_func=test_validate_zip,
        description="Validate ZIP file tests",
    )

    # Run tests
    framework.run_tests()

    # Summarize results
    framework.summarize_results()

    # Generate Autolab-compatible results
    auto_results = framework.get_autoresults(RUBRIC)

    # REQUIRED: print exactly one JSON object
    print(json.dumps(auto_results))


###############################################################################
# Entrypoint
###############################################################################

if __name__ == "__main__":
    main()
