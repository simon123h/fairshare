# Architecture of FairShare CLI

This document describes the high-level architecture and project structure of FairShare CLI.

## Project Structure

- `fairshare/`: The core Python package.
  - `expense.py`: Data model for individual expenses.
  - `ledger.py`: The main logic (Aggregate) for managing participants and calculating balances.
  - `report_generator.py`: Responsible for generating the Markdown report.
  - `wizard.py`: Implementation of the interactive initialization wizard.
  - `i18n.py`: Internationalization support and language detection.
  - `locales/`: YAML files containing translations for various languages.
- `fairshare-data/`: Directory where all user settlement files (`*.costs.yaml`) are stored.
- `tests/`: Comprehensive unit tests covering domain logic, validations, and i18n.
- `run.py`: The entry point script that orchestrates the CLI flow.

## Design Principles

- **Separation of Concerns:** Domain logic is kept separate from the CLI presentation layer.
- **i18n First:** All user-facing strings are externalized into locale files.
- **Data Integrity:** Strict validation ensures that expenses and participant lists are always in a consistent state.

## Data Format

Project data is stored in YAML files within the `fairshare-data/` directory.

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
    # If omitted, the expense is split among ALL participants.
    split_among:
      - Alice
      - Bob
```
