# Define the name of the virtual environment directory
VENV_DIR = venv

# Define the Python interpreter to use
PYTHON = python3

# Define the requirements file
REQUIREMENTS = requirements.txt

# Create the virtual environment
$(VENV_DIR)/bin/activate: $(REQUIREMENTS)
    $(PYTHON) -m venv $(VENV_DIR)
    $(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

# Activate the virtual environment
activate:
    @echo "Run 'source $(VENV_DIR)/bin/activate' to activate the virtual environment."

# Clean the virtual environment
clean:
    rm -rf $(VENV_DIR)

# Default target
all: $(VENV_DIR)/bin/activate

.PHONY: activate clean all