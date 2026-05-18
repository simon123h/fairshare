import argparse

import yaml

from fairshare.expense import Expense
from fairshare.ledger import Ledger
from fairshare.report_generator import ReportGenerator


def main():
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
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        participants = data.get("participants", [])
        expenses_data = data.get("expenses", [])

        # Initialisierung des Ledgers
        ledger = Ledger(participants)

        # Hinzufügen der Ausgaben
        for e_data in expenses_data:
            expense = Expense(
                payer=e_data["payer"],
                amount=e_data["amount"],
                description=e_data.get("description", "Ausgabe"),
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
