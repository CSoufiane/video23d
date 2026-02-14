.PHONY: setup test run clean

# Default target
all: setup

# Install everything
setup:
	chmod +x setup.sh
	./setup.sh
	mkdir -p frames output data/raw

# Run BDD tests
test:
	PYTHONPATH=. ./venv/bin/pytest tests/step_definitions/

# Run the full 3D pipeline (US-22)
run:
	PYTHONPATH=. ./venv/bin/python main.py

# Clean temporary files
clean:
	rm -f camera_calib.yaml
	rm -rf frames/*
	rm -rf output/*
	find . -type d -name "__pycache__" -exec rm -rf {} +

tree:
	tree -I '.git/|output/|.pytest_cache|venv/|__pycache__|data/|frames/'