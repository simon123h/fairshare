import sys
from typing import Any, Dict, List, Optional

import questionary
import yaml
from questionary import Style

from .i18n import _


class InteractiveWizard:
    """
    An interactive wizard for creating or updating project files.
    Uses 'questionary' with customized i18n styles.
    """

    # Custom style for prompts
    custom_style = Style(
        [
            ("qmark", "fg:#673ab7 bold"),  # The prefix character (our '>')
            ("question", "bold"),  # The actual question
            ("answer", "fg:#f44336 bold"),  # The given answer
            ("pointer", "fg:#673ab7 bold"),  # The selection pointer
            ("highlighted", "fg:#673ab7 bold"),  # Highlighted text
            ("selected", "fg:#ccff00"),  # Selected option
            ("instruction", "fg:#888888"),  # Help texts
        ]
    )

    @staticmethod
    def run(output_path: str, existing_data: Optional[Dict[str, Any]] = None) -> None:
        if existing_data:
            participants = existing_data.get("participants", [])
            expenses = existing_data.get("expenses", [])
        else:
            # 1. Ask for participants
            while True:
                p_input = questionary.text(
                    _("wizard.participants.q"),
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                ).ask()

                if p_input is None:
                    sys.exit(0)

                participants = [p.strip() for p in p_input.split(",") if p.strip()]
                if participants:
                    break
                print(_("wizard.participants.error_min"))

            expenses = []

        # 2. Ask for expenses
        print(f"\n{_('wizard.expenses.header')}")
        while True:
            # Payer selection via list
            payer_options = [_("wizard.finish")] + participants
            payer = questionary.select(
                _("wizard.expenses.payer_q"),
                choices=payer_options,
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction=_("wizard.expenses.payer_inst"),
            ).ask()

            if payer is None or payer == _("wizard.finish"):
                break

            # Ask for amount
            while True:
                amount_str = questionary.text(
                    _("wizard.expenses.amount_q"),
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                ).ask()
                if amount_str is None:
                    sys.exit(0)

                try:
                    amount = float(amount_str.replace(",", "."))
                    if amount < 0:
                        print(_("wizard.expenses.neg_amount_error"))
                        continue
                    break
                except ValueError:
                    print(_("wizard.expenses.amount_error"))

            description = questionary.text(
                _("wizard.expenses.desc_q"),
                qmark=">",
                style=InteractiveWizard.custom_style,
            ).ask()
            if description is None:
                sys.exit(0)

            # Determine split
            split_type = questionary.select(
                _("wizard.split.q"),
                choices=[
                    _("wizard.split.all"),
                    _("wizard.split.custom"),
                ],
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction=_("wizard.split.inst"),
            ).ask()

            if split_type is None:
                sys.exit(0)

            split_among: Optional[List[str]] = None
            if split_type == _("wizard.split.custom"):
                split_among = questionary.checkbox(
                    _("wizard.checkbox.q"),
                    choices=participants,
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                    instruction=_("wizard.checkbox.inst"),
                ).ask()

                if split_among is None:
                    sys.exit(0)

                if not split_among:
                    print(_("wizard.checkbox.error_min"))
                    split_among = None

            expense_dict: Dict[str, Any] = {
                "payer": payer,
                "amount": amount,
                "description": description,
            }
            if split_among:
                expense_dict["split_among"] = split_among

            expenses.append(expense_dict)

        # 3. Save
        data = {"participants": participants, "expenses": expenses}

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            print(f"\n{_('wizard.success', path=output_path)}")
        except Exception as e:
            print(_("error.unexpected", exc=e))
