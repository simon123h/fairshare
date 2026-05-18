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
# Nutzt standardmäßig 'costs.yaml'
python3 run.py
```bash
# Oder geben Sie einen spezifischen Pfad an
python3 run.py meine_kosten.yaml
```

Das Skript generiert automatisch einen Markdown-Bericht (`report.md`), der eine tabellarische Zusammenfassung und alle Details enthält.

### PDF-Export mit Pandoc

Sie können den generierten Markdown-Bericht mit **Pandoc** in ein PDF konvertieren. Mit der Option `-V geometry:margin=2cm` lassen sich die Seitenränder anpassen:

```bash
# Einfache Konvertierung
pandoc report.md -V geometry:margin=2cm -o abrechnung.pdf

# Via LaTeX (für ein professionelleres Layout, benötigt xelatex)
pandoc report.md -V geometry:margin=2cm -o abrechnung.pdf --pdf-engine=xelatex
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

Die Eingabedaten werden in der Datei `costs.yaml` verwaltet. Eine Vorlage finden Sie in `costs.yaml.example`.

### Struktur

```yaml
# Liste aller Personen, die standardmäßig an allen Ausgaben beteiligt sind
participants:
  - Name1
  - Name2
  - Name3

# Liste der einzelnen Ausgaben
expenses:
  - payer: Name1          # Wer hat bezahlt?
    amount: 50.0          # Wie viel wurde bezahlt?
    description: "Einkauf" # Optional: Was wurde gekauft?
    
    # Optional: Nur unter bestimmten Personen aufteilen.
    # Wenn dieses Feld fehlt, wird die Ausgabe unter ALLEN Teilnehmern
    # aus der obigen 'participants' Liste aufgeteilt.
    split_among:
      - Name1
      - Name2
```

### Beispiel

Ein ausführliches Beispiel mit verschiedenen Szenarien (vollständige Aufteilung vs. Teil-Aufteilung) finden Sie in der Datei [costs.yaml.example](costs.yaml.example).
