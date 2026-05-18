from typing import Any, Dict, List

from .expense import Expense
from .i18n import _


class Ledger:
    """
    Verwaltet eine Gruppe von Teilnehmern und deren Ausgaben.
    Berechnet die daraus resultierenden Bilanzen und notwendigen Ausgleichszahlungen.
    """

    def __init__(self, participants: List[str]):
        if not participants:
            raise ValueError(_("val.empty_ledger"))

        # Validierung: Keine leeren Strings als Namen
        if any(not p or not isinstance(p, str) for p in participants):
            raise ValueError(_("val.invalid_names"))

        self.participants = participants
        self.expenses: List[Expense] = []

    def add_expense(self, expense: Expense) -> None:
        """
        Fügt eine neue Ausgabe zum Ledger hinzu.
        Validiert, ob Zahler und Empfänger Teil der Teilnehmergruppe sind.
        """
        # Fail-Fast: Ist der Zahler in der Gruppe?
        if expense.payer not in self.participants:
            raise ValueError(
                _("val.payer_not_in_group", payer=expense.payer, list=self.participants)
            )

        # Fail-Fast: Sind alle spezifischen Empfänger in der Gruppe?
        if expense.split_among:
            for person in expense.split_among:
                if person not in self.participants:
                    raise ValueError(
                        _("val.beneficiary_not_in_group", person=person, desc=expense.description)
                    )

        self.expenses.append(expense)

    def calculate_balances(self) -> Dict[str, float]:
        """
        Berechnet die Netto-Bilanz für jeden Teilnehmer.
        Positiv: Person bekommt Geld. Negativ: Person schuldet Geld.
        """
        balances = {p: 0.0 for p in self.participants}

        for e in self.expenses:
            # Gutschrift für den Zahler
            balances[e.payer] += e.amount

            # Belastung für die Nutznießer
            share = e.calculate_share(self.participants)
            beneficiaries = e.get_beneficiaries(self.participants)
            for b in beneficiaries:
                balances[b] -= share

        return balances

    def get_settlements(self) -> List[Dict[str, Any]]:
        """
        Ermittelt die minimalen Transaktionen, um alle Bilanzen auszugleichen.
        """
        balances = self.calculate_balances()

        debtors: List[List[Any]] = []
        creditors: List[List[Any]] = []
        for p, b in balances.items():
            if b < -0.01:
                debtors.append([p, abs(b)])
            elif b > 0.01:
                creditors.append([p, b])

        settlements: List[Dict[str, Any]] = []
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor_name: str = debtors[i][0]
            debt_amount: float = debtors[i][1]
            creditor_name: str = creditors[j][0]
            credit_amount: float = creditors[j][1]

            settle_amount = min(debt_amount, credit_amount)
            if settle_amount > 0.01:
                settlements.append(
                    {"from": debtor_name, "to": creditor_name, "amount": round(settle_amount, 2)}
                )

            debtors[i][1] -= settle_amount
            creditors[j][1] -= settle_amount

            if debtors[i][1] < 0.01:
                i += 1
            if creditors[j][1] < 0.01:
                j += 1

        return settlements
