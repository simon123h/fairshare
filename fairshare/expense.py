from typing import List, Optional


class Expense:
    """
    Repräsentiert eine einzelne Ausgabe.
    Kapselt Daten und Logik für die Aufteilung.
    """

    def __init__(
        self,
        payer: str,
        amount: float,
        description: str = "Ausgabe",
        split_among: Optional[List[str]] = None,
    ):
        if amount < 0:
            raise ValueError(
                f"Ungültiger Betrag: {amount:.2f}€. Beträge dürfen nicht negativ sein."
            )

        if not payer or not isinstance(payer, str):
            raise ValueError("Ein gültiger Name für den Zahler muss angegeben werden.")

        self.payer = payer
        self.amount = float(amount)
        self.description = description
        self.split_among = split_among

    def get_beneficiaries(self, default_participants: List[str]) -> List[str]:
        """Gibt die Liste der Personen zurück, die an dieser Ausgabe beteiligt sind."""
        beneficiaries = self.split_among if self.split_among else default_participants
        if not beneficiaries:
            raise ValueError(
                f"Ausgabe '{self.description}' hat keine Empfänger (Teilnehmerliste leer)."
            )
        return beneficiaries

    def calculate_share(self, default_participants: List[str]) -> float:
        """Berechnet den Betrag, den jede beteiligte Person für diese Ausgabe tragen muss."""
        beneficiaries = self.get_beneficiaries(default_participants)
        return self.amount / len(beneficiaries)

    def __str__(self) -> str:
        """Erzeugt eine lesbare Zusammenfassung der Ausgabe."""
        split_info = f" (geteilt unter: {', '.join(self.split_among)})" if self.split_among else ""
        return f"{self.payer} hat {self.amount:.2f}€ für '{self.description}' bezahlt{split_info}"
