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

- **Select a project:** Choose from existing `*.costs.yaml` files in the `fairshare-data/` directory.
- **Create a new project:** Select the `[FairShare Initialization Wizard]` option and enter a name. The file will be saved in the `fairshare-data/` directory.

**Note:** The tool automatically appends the `.costs.yaml` extension to project names. All project data is stored in the `fairshare-data/` folder.

After each run, the script automatically generates a detailed Markdown report (`report.md`) in the current directory.

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
