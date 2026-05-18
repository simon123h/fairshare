# Building FairShare CLI

This document explains how to compile the FairShare CLI into a standalone executable for distribution.

## Prerequisites

- Python 3.8 or higher
- All project dependencies installed (`pip install -r requirements.txt`)
- PyInstaller installed (`pip install pyinstaller`)

## Compilation with PyInstaller

We use a cross-platform `.spec` file to manage the build configuration. This ensures that translation resources and dependencies are correctly bundled regardless of the operating system.

### Recommended: Building from the Spec File

Run the following command from the project root:

```bash
pyinstaller fairshare.spec
```

This command works on Linux, macOS, and Windows. It automatically:

- Bundles the application into a single executable (`--onefile`).
- Includes all translation files from `fairshare/locales`.
- Names the output binary `fairshare` (or `fairshare.exe` on Windows).

### Alternative: Manual Command Line

If you do not want to use the `.spec` file, you must manually specify the data paths (note the separator difference between platforms):

**Linux / macOS**

```bash
pyinstaller --onefile --name fairshare --add-data "fairshare/locales:fairshare/locales" run.py
```

**Windows**

```bash
pyinstaller --onefile --name fairshare --add-data "fairshare/locales;fairshare/locales" run.py
```

## Output

The resulting binary will be placed in the `dist/` directory:

- Linux/macOS: `dist/fairshare`
- Windows: `dist/fairshare.exe`

## Note on `.spec` Files

The `fairshare.spec` file is a Python script that defines the build process. It is committed to the repository to ensure reproducible builds across different development environments and CI/CD pipelines.
