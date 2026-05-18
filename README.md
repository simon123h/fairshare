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

## Sprache / Multi-language Support

FairShare erkennt automatisch die Systemsprache und passt die Benutzeroberfläche (CLI), den interaktiven Assistenten und die generierten Berichte entsprechend an. Aktuell werden unterstützt:

- **Deutsch** (Standard bei deutscher Systemumgebung)
- **Englisch** (Standard bei allen anderen Umgebungen)

## Installation

Stellen Sie sicher, dass Python installiert ist, und installieren Sie die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Nutzung

Das Programm kann entweder mit einer bestehenden Datei oder interaktiv gestartet werden.

### Bestehende Datei abrechnen

```bash
# Nutzt standardmäßig 'costs.yaml'
python3 run.py

# Oder geben Sie einen spezifischen Pfad an
python3 run.py mein-trip.costs.yaml
```

### Interaktiver Assistent zum Erstellen einer neuen Datei

Wenn Sie eine neue Abrechnung starten möchten, hilft Ihnen der interaktive Assistent:

```bash
# Erstellt/Initialisiert die Standard-Datei 'costs.yaml'
python3 run.py --init

# Erstellt eine benannte Abrechnung (z.B. 'urlaub.costs.yaml')
python3 run.py urlaub --init
```

**Besonderheit:** Das Tool hängt automatisch die Endung `.costs.yaml` an, falls keine Dateiendung angegeben wird. Dies stellt sicher, dass Ihre privaten Daten gemäß der [Git-Konvention](#sicherheit--privatsphäre) geschützt sind.

Das Skript generiert nach jedem Lauf automatisch einen detaillierten Markdown-Bericht (`report.md`) im aktuellen Verzeichnis.

## Sicherheit & Privatsphäre

Um zu verhindern, dass persönliche Finanzdaten versehentlich in Git-Repositories veröffentlicht werden, nutzt FairShare folgende Sicherheitsmechanismen:

1. **Git-Ignore**: Die Datei `.gitignore` ist so vorkonfiguriert, dass die Standarddatei `costs.yaml` sowie alle Dateien mit der Endung `*.costs.yaml` ignoriert werden.
2. **Namenskonvention**: Nutzen Sie für Ihre Abrechnungen immer die Endung `.costs.yaml` (oder lassen Sie das Tool diese beim `--init` automatisch hinzufügen), damit Ihre Daten lokal auf Ihrem Rechner bleiben.
3. **Beispiele**: Nutzen Sie `costs.yaml.example` als Vorlage für neue Dateien.

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
  - payer: Name1 # Wer hat bezahlt?
    amount: 50.0 # Wie viel wurde bezahlt?
    description: "Einkauf" # Optional: Was wurde gekauft?

    # Optional: Nur unter bestimmten Personen aufteilen.
    # Wenn dieses Feld fehlt, wird die Ausgabe unter ALLEN Teilnehmern
    # aus der obigen 'participants' Liste aufgeteilt.
    split_among:
      - Name1
      - Name2
```

Ein ausführliches Beispiel mit verschiedenen Szenarien finden Sie in der Datei [costs.yaml.example](costs.yaml.example).
