import sys
from typing import Any, Dict, List, Optional

import questionary
import yaml
from questionary import Style


class InteractiveWizard:
    """
    Ein interaktiver Assistent zum Erstellen einer neuen Kosten-Datei.
    Nutzt 'questionary' mit angepasstem deutschen Stil.
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
        print("\n=== FairShare Initialisierungs-Assistent ===\n")

        # 1. Teilnehmer abfragen
        while True:
            p_input = questionary.text(
                "Wer nimmt an der Abrechnung teil? (Namen mit Komma getrennt):",
                qmark=">",
                style=InteractiveWizard.custom_style,
            ).ask()

            if p_input is None:
                sys.exit(0)

            participants = [p.strip() for p in p_input.split(",") if p.strip()]
            if participants:
                break
            print("Fehler: Mindestens ein Teilnehmer muss angegeben werden.")

        expenses: List[Dict[str, Any]] = []

        # 2. Ausgaben abfragen
        print("\n--- Ausgaben erfassen ---")
        while True:
            # Auswahl des Zahlers per Liste
            payer_options = ["(Beenden und Speichern)"] + participants
            payer = questionary.select(
                "Wer hat bezahlt?",
                choices=payer_options,
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction="(Nutze die Pfeiltasten zum Auswählen)",
            ).ask()

            if payer is None or payer == "(Beenden und Speichern)":
                break

            # Betrag abfragen
            while True:
                amount_str = questionary.text(
                    "Betrag in €:",
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                ).ask()
                if amount_str is None:
                    sys.exit(0)

                try:
                    amount = float(amount_str.replace(",", "."))
                    if amount < 0:
                        print("Fehler: Der Betrag darf nicht negativ sein.")
                        continue
                    break
                except ValueError:
                    print("Fehler: Bitte eine gültige Zahl eingeben.")

            description = questionary.text(
                "Beschreibung (optional):",
                qmark=">",
                style=InteractiveWizard.custom_style,
            ).ask()
            if description is None:
                sys.exit(0)

            # Aufteilung festlegen
            split_type = questionary.select(
                "Wie soll der Betrag aufgeteilt werden?",
                choices=[
                    "Unter ALLEN Teilnehmern",
                    "Nur unter bestimmten Personen auswählen",
                ],
                qmark=">",
                style=InteractiveWizard.custom_style,
                instruction="(Pfeiltasten zur Auswahl)",
            ).ask()

            if split_type is None:
                sys.exit(0)

            split_among: Optional[List[str]] = None
            if split_type == "Nur unter bestimmten Personen auswählen":
                split_among = questionary.checkbox(
                    "Wähle die Personen aus, die sich diese Ausgabe teilen:",
                    choices=participants,
                    qmark=">",
                    style=InteractiveWizard.custom_style,
                    instruction="(Leertaste zum Markieren, Eingabe zum Bestätigen)",
                ).ask()

                if split_among is None:
                    sys.exit(0)

                if not split_among:
                    print("Fehler: Mindestens eine Person muss ausgewählt werden. Standard: Alle.")
                    split_among = None

            expense_dict: Dict[str, Any] = {
                "payer": payer,
                "amount": amount,
                "description": description,
            }
            if split_among:
                expense_dict["split_among"] = split_among

            expenses.append(expense_dict)

            print()

        # 3. Speichern
        data = {"participants": participants, "expenses": expenses}

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            print(f"\nErfolg: Die Datei '{output_path}' wurde erstellt!")
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")
