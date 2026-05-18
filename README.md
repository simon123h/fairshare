# FairShare CLI

A simple Python tool to fairly split expenses among multiple people.

## Installation

Ensure you have Python installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The program must be started with a project name or a path to a file. It can also be used interactively to create a new project.

### Processing an Existing Project

```bash
# Specify the project name
python3 run.py my-trip
```

### Interactive Wizard for Creating a New Project

If you want to start a new settlement, use the interactive wizard:

```bash
# Creates/Initializes a project
python3 run.py vacation --init
```

**Note:** The tool automatically appends the `.costs.yaml` extension to the data file. This ensures all data files are ignored from the git repository.

After each run, the script automatically generates a detailed Markdown report (`report.md`) in the current directory.

## YAML Format

Input data is managed in YAML files (e.g., `my-trip.costs.yaml`).

```yaml
# List of all people participating by default
participants:
  - Alice
  - Bob
  - Charlie

# List of individual expenses
expenses:
  - payer: Alice
    amount: 50.0
    description: "Groceries"

    # Optional: Split among specific people only.
    split_among:
      - Alice
      - Bob
```

See [costs.yaml.example](costs.yaml.example) for a detailed example.

## Language Support

FairShare automatically detects your system language and adjusts the CLI, interactive wizard, and generated reports accordingly. Currently supported languages:

- **English** (Default)
- **German** (Deutsch)
- **French** (Français)
- **Lithuanian** (Lietuvių)
- **Japanese** (日本語)
- **Chinese** (中文)

## PDF Export

You can convert the generated Markdown report to PDF using **Pandoc**:

```bash
pandoc report.md -V geometry:margin=2cm -o settlement.pdf
```

---

_For development, project structure, or contributing, please see [ARCHITECTURE.md](ARCHITECTURE.md) and [CONTRIBUTING.md](CONTRIBUTING.md)._
