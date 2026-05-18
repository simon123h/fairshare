import argparse
import sys
from typing import Any, Dict, List

import yaml

from fairshare.expense import Expense
from fairshare.ledger import Ledger
from fairshare.report_generator import ReportGenerator
from fairshare.wizard import InteractiveWizard


def main() -> None:
    parser = argparse.ArgumentParser(description="FairShare: Kosten unter Personen aufteilen.")
    parser.add_argument(
        "file",
        nargs="?",
        default="costs.yaml",
        help="Pfad zur YAML-Datei mit den Ausgaben (Standard: costs.yaml)",
    )
    parser.add_argument(
        "--report", default="report.md", help="Pfad für den Markdown-Bericht (Standard: report.md)"
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Startet den interaktiven Assistenten zum Erstellen einer neuen Datei.",
    )
    args = parser.parse_args()

    # Automatisches Suffix hinzufügen, falls es fehlt und es keine .example Datei ist
    input_file = args.file
    if (
        not input_file.endswith(".costs.yaml")
        and not input_file.endswith(".yaml")
        and not input_file.endswith(".yml")
    ):
        input_file += ".costs.yaml"
    elif (
        input_file.endswith(".yaml")
        and not input_file.endswith(".costs.yaml")
        and not input_file.endswith(".example")
    ):
        # Optional: Konvertiere .yaml zu .costs.yaml für bessere Git-Ignorierung,
        # aber nur wenn vom User gewünscht. Hier bleiben wir bei der expliziten Logik:
        pass

    # Interaktiver Modus
    if args.init:
        InteractiveWizard.run(input_file)
        sys.exit(0)

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not data:
            print(f"Fehler: Die Datei '{input_file}' ist leer.")
            return

        participants: List[str] = data.get("participants", [])
        expenses_data: List[Dict[str, Any]] = data.get("expenses", [])

        # Initialisierung des Ledgers
        ledger = Ledger(participants)

        # Hinzufügen der Ausgaben
        for e_data in expenses_data:
            expense = Expense(
                payer=e_data["payer"],
                amount=e_data["amount"],
                description=e_data.get("description", None),
                split_among=e_data.get("split_among"),
            )
            ledger.add_expense(expense)

        if not participants and not ledger.expenses:
            print(f"Fehler: Keine Teilnehmer oder Ausgaben in '{args.file}' gefunden.")
            return

        # Konsolen-Ausgabe
        print(f"Teilnehmer: {', '.join(participants)}")
        total = sum(e.amount for e in ledger.expenses)
        print(f"\nGesamtausgaben: {total:.2f}€")

        balances = ledger.calculate_balances()
        paid_amounts = {p: 0.0 for p in balances.keys()}
        for e in ledger.expenses:
            paid_amounts[e.payer] += e.amount

        print(f"\n{'Name':<15} | {'Bezahlt':>12} | {'Soll-Anteil':>12} | {'Differenz':>12}")
        print(f"{'-' * 60}")
        for person in sorted(balances.keys()):
            paid = paid_amounts[person]
            diff = balances[person]
            share = paid - diff
            sign = "+" if diff > 0.005 else "-" if diff < -0.005 else " "
            print(f"{person:<15} | {paid:>10.2f} € | {share:>10.2f} € | {sign} {abs(diff):>8.2f} €")
        print(f"{'=' * 60}")

        settlements = ledger.get_settlements()
        if not settlements:
            print("\nAlles bereits ausgeglichen!")
        else:
            print("\nVorgeschlagene Zahlungen zum Ausgleich:")
            for s in settlements:
                print(f"  {s['from']} zahlt {s['amount']:.2f}€ an {s['to']}")

        # Bericht-Generierung
        ReportGenerator.generate_markdown(ledger, settlements, args.report)
        print(f"\nMarkdown-Bericht wurde erstellt: {args.report}")

    except FileNotFoundError:
        print(f"Fehler: Die Datei '{args.file}' wurde nicht gefunden.")
    except yaml.YAMLError as exc:
        print(f"Fehler beim Lesen der YAML-Datei: {exc}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()
