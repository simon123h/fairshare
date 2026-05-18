from typing import List, Optional

from .i18n import _


class Expense:
    """
    Repräsentiert eine einzelne Ausgabe.
    Kapselt Daten und Logik für die Aufteilung.
    """

    def __init__(
        self,
        payer: str,
        amount: float,
        description: str = "",
        split_among: Optional[List[str]] = None,
    ) -> None:
        if amount < 0:
            raise ValueError(_("val.neg_amount", amount=amount))

        if not payer or not isinstance(payer, str):
            raise ValueError(_("val.invalid_payer"))

        self.payer = payer
        self.amount = float(amount)
        self.description = description
        self.split_among = split_among

    def get_beneficiaries(self, default_participants: List[str]) -> List[str]:
        """Gibt die Liste der Personen zurück, die an dieser Ausgabe beteiligt sind."""
        beneficiaries = self.split_among if self.split_among else default_participants
        if not beneficiaries:
            raise ValueError(_("val.empty_beneficiaries", desc=self.description))
        return beneficiaries

    def calculate_share(self, default_participants: List[str]) -> float:
        """Berechnet den Betrag, den jede beteiligte Person für diese Ausgabe tragen muss."""
        beneficiaries = self.get_beneficiaries(default_participants)
        return self.amount / len(beneficiaries)

    def __str__(self) -> str:
        """Erzeugt eine lesbare Zusammenfassung der Ausgabe."""
        split_info = ""
        if self.split_among:
            split_info = f" ({_('table.split')}: {', '.join(self.split_among)})"

        # Übersetzungsteile abrufen
        p_label = _("core.paid").lower()
        d_label = _("table.desc").lower()

        return (
            f"{self.payer} {p_label} {self.amount:.2f}€ {d_label} '{self.description}'{split_info}"
        )
