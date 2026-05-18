import argparse
from typing import Any, Dict, List

import yaml

from fairshare.expense import Expense
from fairshare.i18n import _
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

    # Interaktiver Modus
    if args.init:
        InteractiveWizard.run(input_file)
        # Wir fahren fort, um die Datei direkt abzurechnen und den Bericht zu erstellen

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not data:
            print(_("error.empty", path=input_file))
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
                description=e_data.get("description", _("wizard.expenses.desc_default")),
                split_among=e_data.get("split_among"),
            )
            ledger.add_expense(expense)

        if not participants and not ledger.expenses:
            print(_("error.empty", path=input_file))
            return

        # Konsolen-Ausgabe
        print(f"{_('core.participants')}: {', '.join(participants)}")
        total = sum(e.amount for e in ledger.expenses)
        print(f"\n{_('core.total_spent')}: {total:.2f}€")

        balances = ledger.calculate_balances()
        paid_amounts = {p: 0.0 for p in balances.keys()}
        for e in ledger.expenses:
            paid_amounts[e.payer] += e.amount

        # Header-Labels abrufen für Tabellenausrichtung
        h_name, h_paid = _("core.name"), _("core.paid")
        h_share, h_diff = _("core.share"), _("core.diff")

        print(f"\n{h_name:<15} | {h_paid:>12} | {h_share:>12} | {h_diff:>12}")
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
            print(f"\n{_('core.settled_msg')}")
        else:
            print(f"\n{_('core.settlements_header')}:")
            for s in settlements:
                print(f"  {_('core.pays_to', from_p=s['from'], amount=s['amount'], to_p=s['to'])}")

        # Bericht-Generierung
        ReportGenerator.generate_markdown(ledger, settlements, args.report)
        print(f"\n{_('core.report_created', path=args.report)}")

    except FileNotFoundError:
        print(_("error.not_found", path=input_file))
    except yaml.YAMLError as exc:
        print(_("error.yaml", exc=exc))
    except Exception as e:
        print(_("error.unexpected", exc=e))


if __name__ == "__main__":
    main()
