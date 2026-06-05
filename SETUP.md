# Setup & Development

## Prerequisites
- Python 3.9+ (recommended 3.11+)
- Poetry

## Installation

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Activate virtual environment**:
   ```bash
   poetry shell
   ```
   Or run commands with `poetry run`:
   ```bash
   poetry run python your_script.py
   ```

## Development

### Run tests
```bash
poetry run pytest
```

### Format code
```bash
poetry run black .
poetry run isort .
```

### Lint & type check
```bash
poetry run flake8 .
poetry run mypy .
```

## Update dependencies
```bash
poetry update
```

This will update all dependencies while respecting the constraints in `pyproject.toml` and regenerate `poetry.lock`.

## Lock file
The `poetry.lock` file contains exact versions of all dependencies (including transitive). Commit this to version control for reproducible installs.
