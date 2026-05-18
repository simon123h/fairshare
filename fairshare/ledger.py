from typing import Dict, List

from .expense import Expense


class Ledger:
    """
    Verwaltet eine Gruppe von Teilnehmern und deren Ausgaben.
    Berechnet die daraus resultierenden Bilanzen und notwendigen Ausgleichszahlungen.
    """

    def __init__(self, participants: List[str]):
        self.participants = participants
        self.expenses: List[Expense] = []

    def add_expense(self, expense: Expense):
        """Fügt eine neue Ausgabe zum Ledger hinzu."""
        self.expenses.append(expense)

    def calculate_balances(self) -> Dict[str, float]:
        """
        Berechnet die Netto-Bilanz für jeden Teilnehmer.
        Positiv: Person bekommt Geld. Negativ: Person schuldet Geld.
        """
        # Alle involvierten Personen (Initialteilnehmer + alle aus den Ausgaben)
        all_people = set(self.participants)
        for e in self.expenses:
            all_people.add(e.payer)
            if e.split_among:
                all_people.update(e.split_among)

        balances = {p: 0.0 for p in all_people}

        for e in self.expenses:
            # Gutschrift für den Zahler
            balances[e.payer] += e.amount

            # Belastung für die Nutznießer
            share = e.calculate_share(self.participants)
            beneficiaries = e.get_beneficiaries(self.participants)
            for b in beneficiaries:
                balances[b] -= share

        return balances

    def get_settlements(self) -> List[Dict]:
        """
        Ermittelt die minimalen Transaktionen, um alle Bilanzen auszugleichen.
        """
        balances = self.calculate_balances()

        debtors = []
        creditors = []
        for p, b in balances.items():
            if b < -0.01:
                debtors.append([p, abs(b)])
            elif b > 0.01:
                creditors.append([p, b])

        settlements = []
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor_name, debt_amount = debtors[i]
            creditor_name, credit_amount = creditors[j]

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
