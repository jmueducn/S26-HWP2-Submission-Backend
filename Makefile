# Directories
HANDIN_FILE = handin.zip
TEST_DIR = autolab
AUTOGRADE_FILES = $(TEST_DIR)/testing_framework.py $(TEST_DIR)/runner.py

.SUFFIXES:          # Disable implicit rules

# Python command
# python3 for autolab
PYTHON = python3

# Default target (when 'make' is run without arguments)
default: grade

autolab: # Prepare autograder package
	@rm -rf autograde.tar autograde-Makefile
	@make create_autograde
	@cp Makefile autograde-Makefile
	@echo "Autograder package prepared."

simulate: # Simulate autograder locally
	@echo "Simulating autograder locally..."
	@rm -rf autograde.tar dummy_submission.zip autograde-Makefile autograde_simutation
	@make create_autograde
	@cp Makefile autograde-Makefile
	@make dummy_submission
	@echo "Simulating autograder..."
	@python simulate_autolab.py dummy_submission.zip
	@rm -rf dummy_submission.zip autograde_simulation autograde-Makefile autograde.tar
	@echo "Simulation complete."
 
# Create autograde.tar containing all test files and dependencies
create_autograde:
	@echo "Creating autograde.tar..."
	@tar --exclude='*.pyc' \
		--exclude='__pycache__' \
		--exclude='mytorch' \
		--exclude='*.ipynb' \
		-cvzf autograde.tar $(AUTOGRADE_FILES)
	@echo "Created autograde.tar successfully"

# Create a dummy submission.zip for testing
dummy_submission:
	@echo "Creating dummy submission.zip..."
	@touch ACKNOWLEDGEMENT.txt README.txt model_metadata.json wandb_export.pkl kaggle_metadata.json
	@zip -r dummy_submission.zip ACKNOWLEDGEMENT.txt README.txt model_metadata.json wandb_export.pkl kaggle_metadata.json
	@rm ACKNOWLEDGEMENT.txt README.txt model_metadata.json wandb_export.pkl kaggle_metadata.json
	@echo "Created dummy_submission.zip successfully"


# Extract autograde.tar
setup:
	@echo "Setting up grading environment..."
	@tar xf autograde.tar
	@mv $(TEST_DIR)/* ./
	@rm -rf $(TEST_DIR)
	@echo "Setup complete."

# Run the tests
grade: setup
	@echo "Running tests..."
	@$(PYTHON) ./runner.py

# Clean up
clean:
	@rm -f *.pyc
	@rm -rf __pycache__
	@rm -rf $(TEST_DIR)/__pycache__

.PHONY: default create_autograde setup grade clean
