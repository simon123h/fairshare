# FairShare CLI

Ein einfaches Python-Tool, um Kosten unter mehreren Personen fair aufzuteilen.

## Struktur

- `fairshare/`: Das Python-Package mit der Domain-Logik.
  - `expense.py`: Definition der `Expense`-Klasse (Datenmodell).
  - `ledger.py`: Das Hauptbuch (Aggregate) zur Verwaltung von Teilnehmern und Ausgaben.
  - `report_generator.py`: Logik zur Erzeugung des Markdown-Berichts.
- `run.py`: Der Einstiegspunkt für das Programm (CLI-Orchestrierung).
- `costs.yaml.example`: Eine Vorlage für die Eingabedatei.
- `tests/`: Umfassende Unit-Tests für alle Komponenten.

## Installation

Stellen Sie sicher, dass Python installiert ist, und installieren Sie die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Nutzung

Bearbeiten Sie die `costs.yaml` (oder nutzen Sie die Vorlage) und führen Sie das Programm aus:

```bash
# Nutzt standardmäßig 'costs.yaml'
python3 run.py

# Oder geben Sie einen spezifischen Pfad an
python3 run.py meine_kosten.yaml

# Interaktiver Assistent zum Erstellen einer neuen Datei
python3 run.py --init
python3 run.py urlaub.yaml --init
```

Das Skript generiert automatisch einen detaillierten Markdown-Bericht (`report.md`) im aktuellen Verzeichnis.

### PDF-Export mit Pandoc

Sie können den generierten Markdown-Bericht mit **Pandoc** in ein PDF konvertieren. Mit der Option `geometry` lassen sich die Seitenränder für eine bessere Tabellendarstellung anpassen:

```bash
# Einfache Konvertierung
pandoc report.md -V geometry:margin=2cm -o abrechnung.pdf

# Via LaTeX (für ein professionelleres Layout, benötigt xelatex)
pandoc report.md -V geometry:margin=2cm -o abrechnung.pdf --pdf-engine=xelatex
```

## Entwicklung & Qualitätssicherung

### Tests & Coverage

Das Projekt enthält Unit-Tests, um die mathematische Korrektheit der Berechnungen und die Validierungen sicherzustellen.

```bash
# Tests ausführen
python3 -m unittest discover tests

# Testabdeckung prüfen
coverage run -m unittest discover tests
coverage report -m
```

### Linting & Formatierung

Dieses Projekt verwendet **Ruff** für extrem schnelles Linting und automatische Code-Formatierung.

```bash
# Code formatieren
ruff format .

# Linting-Fehler prüfen und automatisch beheben
ruff check . --fix
```

### CI/CD

Das Projekt ist für professionelle Workflows vorbereitet und enthält Konfigurationen für **GitLab CI/CD** (`.gitlab-ci.yml`) und **GitHub Actions** (`.github/workflows/ci.yml`). Bei jedem Push werden automatisch:
1. Das Linting und die Formatierung (Ruff) geprüft.
2. Alle Unit-Tests ausgeführt.
3. Die Code-Coverage ermittelt.

## YAML-Format

Die Eingabedaten werden standardmäßig in `costs.yaml` verwaltet.

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

Ein ausführliches Beispiel mit verschiedenen Szenarien finden Sie in der Datei [costs.yaml.example](costs.yaml.example).
