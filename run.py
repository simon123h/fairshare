import os
from pathlib import Path
from typing import Any, Dict, List

import questionary
import yaml

from fairshare.expense import Expense
from fairshare.i18n import _
from fairshare.ledger import Ledger
from fairshare.report_generator import ReportGenerator
from fairshare.wizard import InteractiveWizard

DATA_DIR = Path("fairshare-data")


def get_available_projects() -> Dict[str, str]:
    """
    Scans the data directory for *.costs.yaml files and returns mapping
    of the format {pretty_name: filename}.
    """
    if not DATA_DIR.exists():
        return {}

    projects = {}
    for file in os.listdir(DATA_DIR):
        if file.endswith(".costs.yaml"):
            pretty_name = file.replace(".costs.yaml", "")
            projects[pretty_name] = file
    return projects


def main() -> None:
    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    projects_map = get_available_projects()
    pretty_names = sorted(projects_map.keys())

    # TUI Choice: Select existing or create new
    new_project_label = f"[{_('tui.new_project')}]"
    choices = [new_project_label] + pretty_names

    choice = questionary.select(
        _("tui.select_project"),
        choices=choices,
        qmark=">",
        style=InteractiveWizard.custom_style,
        instruction=_("tui.select_inst"),
    ).ask()

    if choice is None:
        return

    if choice == new_project_label:
        project_name = questionary.text(
            _("tui.enter_name"),
            qmark=">",
            style=InteractiveWizard.custom_style,
        ).ask()
        if not project_name:
            return
        filename = project_name
        if not filename.endswith(".costs.yaml"):
            filename += ".costs.yaml"
        input_file = DATA_DIR / filename
        data = None
    else:
        input_file = DATA_DIR / projects_map[choice]
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except Exception:
            data = None

    # Always run the wizard
    InteractiveWizard.run(str(input_file), existing_data=data)

    try:
        # Reload the data (it might have been created or updated by the wizard)
        with open(input_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        if not data:
            print(_("error.empty", path=str(input_file)))
            return

        participants: List[str] = data.get("participants", [])
        expenses_data: List[Dict[str, Any]] = data.get("expenses", [])

        # Ledger initialization
        ledger = Ledger(participants)

        # Adding expenses
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

        # Console output
        print(f"{_('core.participants')}: {', '.join(participants)}")
        total = sum(e.amount for e in ledger.expenses)
        print(f"\n{_('core.total_spent')}: {total:.2f}€")

        balances = ledger.calculate_balances()
        paid_amounts = {p: 0.0 for p in balances.keys()}
        for e in ledger.expenses:
            paid_amounts[e.payer] += e.amount

        # Retrieve header labels for table alignment
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

        # Report generation
        ReportGenerator.generate_markdown(ledger, settlements, "report.md")
        print(f"\n{_('core.report_created', path='report.md')}")

    except FileNotFoundError:
        print(_("error.not_found", path=input_file))
    except yaml.YAMLError as exc:
        print(_("error.yaml", exc=exc))
    except Exception as e:
        print(_("error.unexpected", exc=e))


if __name__ == "__main__":
    main()
