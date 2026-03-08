.PHONY: setup test run lint clean

# Default variables
PYTHON := python
PIP := pip
VENV_PATH := venv

help:
	@echo "Available commands:"
	@echo "  setup   : Create virtual environment and install dependencies"
	@echo "  run     : Run the Streamlit app"
	@echo "  test    : Run tests with pytest"
	@echo "  lint    : Run flake8 linter"
	@echo "  clean   : Clean up cache files and virtual environment"

setup:
	$(PYTHON) -m venv $(VENV_PATH)
	./$(VENV_PATH)/Scripts/activate && $(PIP) install --upgrade pip
	./$(VENV_PATH)/Scripts/activate && $(PIP) install -r requirements.txt
	./$(VENV_PATH)/Scripts/activate && $(PIP) install -r requirements-dev.txt

run:
	./$(VENV_PATH)/Scripts/activate && streamlit run app.py

test:
	./$(VENV_PATH)/Scripts/activate && pytest tests/ -v

lint:
	./$(VENV_PATH)/Scripts/activate && flake8 src tests

clean:
	rm -rf __pycache__ .pytest_cache
	rm -rf src/*/__pycache__
	rm -rf tests/*/__pycache__
	rm -rf $(VENV_PATH)
