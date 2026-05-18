# FairShare CLI

A simple Python tool to fairly split expenses among multiple people.

## Installation

Ensure you have Python installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

FairShare features a full Terminal UI. Simply start the program, and it will guide you through selecting an existing project or creating a new one.

```bash
python3 run.py
```

- **Select a project:** Choose from existing `*.costs.yaml` files in the current directory.
- **Create a new project:** Select the `[FairShare Initialization Wizard]` option and enter a name for your new project.

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
