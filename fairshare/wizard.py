import sys
from typing import Any, Dict, List, Optional

import questionary
import yaml
from questionary import Style

from .i18n import _


class InteractiveWizard:
    """
    Ein interaktiver Assistent zum Erstellen einer neuen Kosten-Datei.
    Nutzt 'questionary' mit angepasstem I18N-Stil.
    """

    # Benutzerdefinierter Stil für die Prompts
    custom_style = Style(
        [
            ("qmark", "fg:#673ab7 bold"),  # Das Präfix-Zeichen (unser '>')
            ("question", "bold"),  # Die eigentliche Frage
            ("answer", "fg:#f44336 bold"),  # Die gegebene Antwort
            ("pointer", "fg:#673ab7 bold"),  # Der Auswahl-Pointer
            ("highlighted", "fg:#673ab7 bold"),  # Markierter Text
            ("selected", "fg:#ccff00"),  # Ausgewählte Option
            ("instruction", "fg:#888888"),  # Hilfetexte
        ]
    )

    @staticmethod
    def run(output_path: str) -> None:
        print(f"\n{_('wizard_title')}\n")

        # 1. Teilnehmer abfragen
        while True:
            p_input = questionary.text(
                _("wizard_participants_q"),
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction=_("wizard_participants_inst"),
            ).ask()

            if p_input is None:
                sys.exit(0)

            participants = [p.strip() for p in p_input.split(",") if p.strip()]
            if participants:
                break
            print(_("wizard_min_participants"))

        expenses: List[Dict[str, Any]] = []

        # 2. Ausgaben abfragen
        print(f"\n{_('wizard_expenses_header')}")
        while True:
            # Auswahl des Zahlers per Liste
            payer_options = [_("wizard_finish")] + participants
            payer = questionary.select(
                _("wizard_payer_q"),
                choices=payer_options,
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction=_("wizard_payer_inst"),
            ).ask()

            if payer is None or payer == _("wizard_finish"):
                break

            # Betrag abfragen
            while True:
                amount_str = questionary.text(
                    _("wizard_amount_q"),
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                ).ask()
                if amount_str is None:
                    sys.exit(0)

                try:
                    amount = float(amount_str.replace(",", "."))
                    if amount < 0:
                        print(_("wizard_neg_amount_error"))
                        continue
                    break
                except ValueError:
                    print(_("wizard_amount_error"))

            description = questionary.text(
                _("wizard_desc_q"),
                default=_("wizard_desc_default"),
                qmark=">",
                style=InteractiveWizard.custom_style,
            ).ask()
            if description is None:
                sys.exit(0)

            # Aufteilung festlegen
            split_type = questionary.select(
                _("wizard_split_q"),
                choices=[
                    _("wizard_split_all"),
                    _("wizard_split_custom"),
                ],
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction=_("wizard_split_inst"),
            ).ask()

            if split_type is None:
                sys.exit(0)

            split_among: Optional[List[str]] = None
            if split_type == _("wizard_split_custom"):
                split_among = questionary.checkbox(
                    _("wizard_checkbox_q"),
                    choices=participants,
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                    instruction=_("wizard_checkbox_inst"),
                ).ask()

                if split_among is None:
                    sys.exit(0)

                if not split_among:
                    print(_("wizard_min_beneficiary"))
                    split_among = None

            expense_dict: Dict[str, Any] = {
                "payer": payer,
                "amount": amount,
                "description": description,
            }
            if split_among:
                expense_dict["split_among"] = split_among

            expenses.append(expense_dict)

        # 3. Speichern
        data = {"participants": participants, "expenses": expenses}

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            print(f"\n{_('wizard_success', path=output_path)}")
        except Exception as e:
            print(_("error_unexpected", exc=e))
