import argparse
import yaml

from fairshare.expense import Expense
from fairshare.ledger import Ledger


def main():
    parser = argparse.ArgumentParser(description="FairShare: Kosten unter Personen aufteilen.")
    parser.add_argument(
        "file",
        nargs="?",
        default="costs.yaml",
        help="Pfad zur YAML-Datei mit den Ausgaben (Standard: costs.yaml)",
    )
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        participants = data.get("participants", [])
        expenses_data = data.get("expenses", [])

        # Initialisierung des Ledgers (Domain Aggregate)
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

        print(f"Teilnehmer: {', '.join(participants)}")
        print("Ausgaben:")
        for e in ledger.expenses:
            print(f"  {e}")

        total = sum(e.amount for e in ledger.expenses)
        print(f"\nGesamtausgaben: {total:.2f}€")

        # Berechnung über das Ledger-Objekt
        settlements = ledger.get_settlements()

        if not settlements:
            print("\nAlles ausgeglichen!")
        else:
            print("\nVorgeschlagene Zahlungen zum Ausgleich:")
            for s in settlements:
                print(f"  {s['from']} zahlt {s['amount']:.2f}€ an {s['to']}")

    except FileNotFoundError:
        print(f"Fehler: Die Datei '{args.file}' wurde nicht gefunden.")
    except yaml.YAMLError as exc:
        print(f"Fehler beim Lesen der YAML-Datei: {exc}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()
