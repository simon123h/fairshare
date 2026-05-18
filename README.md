# FairShare CLI

A simple Python tool to fairly split expenses among multiple people.

## Project Structure

- `fairshare/`: The Python package containing the domain logic and i18n resources.
- `tests/`: Comprehensive unit tests for all components.
- `run.py`: The entry point for the application.
- `costs.yaml.example`: A template for the input file.

## Language Support

FairShare automatically detects your system language and adjusts the CLI, interactive wizard, and generated reports accordingly. Currently supported languages:

- **English** (Default)
- **German** (Deutsch)
- **French** (Français)
- **Lithuanian** (Lietuvių)
- **Japanese** (日本語)
- **Chinese** (中文)

## Installation

Ensure you have Python installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The program can be started with an existing file or interactively.

### Processing an Existing File

```bash
# Uses 'costs.yaml' by default
python3 run.py

# Or specify a specific path
python3 run.py my-trip.costs.yaml
```

### Interactive Wizard for Creating a New File

If you want to start a new settlement, use the interactive wizard:

```bash
# Initializes the default file 'costs.yaml'
python3 run.py --init

# Creates a named settlement (e.g., 'vacation.costs.yaml')
python3 run.py vacation --init
```

**Note:** The tool automatically appends the `.costs.yaml` extension if none is provided. This ensures your private data is protected according to the [Security & Privacy](#security--privacy) section.

After each run, the script automatically generates a detailed Markdown report (`report.md`) in the current directory.

## Security & Privacy

To prevent accidental publication of personal financial data in Git repositories, FairShare uses the following mechanisms:

1. **Git-Ignore**: The `.gitignore` file is pre-configured to ignore the default `costs.yaml` and all files ending in `*.costs.yaml`.
2. **Naming Convention**: Always use the `.costs.yaml` extension for your settlements to keep your data local.
3. **Examples**: Use `costs.yaml.example` as a template for new files.

### PDF Export with Pandoc

You can convert the generated Markdown report to PDF using **Pandoc**. Use the `geometry` option to adjust margins for better table display:

```bash
# Basic conversion
pandoc report.md -V geometry:margin=2cm -o settlement.pdf

# Via LaTeX (for a professional layout, requires xelatex)
pandoc report.md -V geometry:margin=2cm -o settlement.pdf --pdf-engine=xelatex
```

## Development & Quality Assurance

### Tests & Coverage

The project includes unit tests to ensure mathematical correctness and valid data handling.

```bash
# Run tests
python3 -m unittest discover tests

# Check test coverage
coverage run -m unittest discover tests
coverage report -m
```

### Linting & Formatting

This project uses **Ruff** for fast linting and automatic code formatting.

```bash
# Format code
ruff format .

# Check and fix linting errors
ruff check . --fix
```

### CI/CD

Configurations for **GitLab CI/CD** (`.gitlab-ci.yml`) and **GitHub Actions** (`.github/workflows/ci.yml`) are included. Each push automatically triggers:

1. Linting and formatting checks (Ruff).
2. Unit tests.
3. Code coverage reports.

## YAML Format

Input data is managed in `costs.yaml`.

### Structure

```yaml
# List of all people participating by default
participants:
  - Name1
  - Name2
  - Name3

# List of individual expenses
expenses:
  - payer: Name1 # Who paid?
    amount: 50.0 # How much?
    description: "Groceries" # Optional

    # Optional: Split among specific people only.
    # If omitted, it is split among ALL participants listed above.
    split_among:
      - Name1
      - Name2
```

See [costs.yaml.example](costs.yaml.example) for a detailed example.
