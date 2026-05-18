# FairShare CLI

Ein einfaches Python-Tool, um Kosten unter mehreren Personen fair aufzuteilen.

## Struktur

- `fairshare/`: Das Python-Package mit der Logik.
  - `expense.py`: Definition der `Expense`-Klasse.
  - `settlement_logic.py`: Der Algorithmus zum Ausgleich der Schulden.
- `run.py`: Der Einstiegspunkt für das Programm.
- `costs.yaml`: Die Eingabedatei für Teilnehmer und Ausgaben.

## Installation

Stellen Sie sicher, dass Python installiert ist, und installieren Sie die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Nutzung

Bearbeiten Sie die `costs.yaml` nach Ihren Bedürfnissen und führen Sie das Programm aus:

```bash
python3 run.py
```

## Tests

Das Projekt enthält Unit-Tests, um die Korrektheit der Berechnungen sicherzustellen. Sie können die Tests mit folgendem Befehl ausführen:

```bash
python3 -m unittest discover tests
```

## Linting & Formatierung

Dieses Projekt verwendet **Ruff** für schnelles Linting und automatische Code-Formatierung.

```bash
# Code formatieren
ruff format .

# Linting-Fehler prüfen und automatisch beheben
ruff check . --fix
```

## CI/CD

Das Projekt enthält Konfigurationen für **GitLab CI/CD** (`.gitlab-ci.yml`) und **GitHub Actions** (`.github/workflows/ci.yml`). Die Pipelines führen automatisch folgende Schritte bei jedem Push aus:
1. **Linting**: Prüfung durch Ruff auf Code-Qualität und Formatierung.
2. **Tests**: Ausführung aller Unit-Tests.


## YAML-Format

```yaml
participants:
  - Name1
  - Name2

expenses:
  - payer: Name1
    amount: 50.0
    description: "Einkauf"
    # Optional: Nur unter bestimmten Personen aufteilen
    split_among:
      - Name1
      - Name2
```
