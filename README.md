# FairShare CLI

A simple Python tool to fairly split expenses among multiple people with a full Terminal UI.

## Quick Start (Executable)

1. **Download** the latest executable for your platform from the releases page.
2. **Run** the application:

   ```bash
   # On Linux/macOS
   ./fairshare

   # On Windows
   fairshare.exe
   ```

## Alternative: Run with Python

If you prefer to run from source, ensure you have Python 3.8+ installed:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the program:**
   ```bash
   python3 run.py
   ```

## Usage

FairShare features a full Terminal UI that guides you through the process:

- **Select a project:** Choose from existing `*.costs.yaml` files in the `fairshare-data/` directory.
- **Create a new project:** Select the `[FairShare Initialization Wizard]` option and enter a name.

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

_For development, project structure, or building the executable, please see [ARCHITECTURE.md](ARCHITECTURE.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [BUILD.md](docs/BUILD.md)._
