.PHONY: reset install test lint run runmod clean

# Remove the virtual environment
reset:
	poetry env remove python3

# Remove build artifacts and caches
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache *.pyc *.pyo *.egg-info dist build

# Install dependencies from pyproject.toml
install:
	poetry install

# Check code style and auto-fix with Ruff (don't fail on warnings)
lint:
	poetry run ruff check src/ --fix || true

# Run the project as a script
run:
	poetry run python src/hive/game.py

# Run the project as a module
runmod:
	poetry run python -m hive.game

# Run all tests using pytest
test:
	poetry run pytest