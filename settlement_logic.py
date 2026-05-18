from typing import List, Dict
from expense import Expense

def calculate_settlements(expenses: List[Expense], participants: List[str]) -> List[Dict]:
    """
    Berechnet die minimalen Transaktionen basierend auf Expense-Objekten.
    """
    # Alle involvierten Personen sammeln (Teilnehmer + alle in den Ausgaben genannten)
    all_people = set(participants)
    for e in expenses:
        all_people.add(e.payer)
        if e.split_among:
            all_people.update(e.split_among)
            
    balances = {p: 0.0 for p in all_people}
    
    for e in expenses:
        # Dem Zahler den vollen Betrag gutschreiben
        balances[e.payer] += e.amount
        
        # Den Nutznießern ihren jeweiligen Anteil abziehen
        share = e.calculate_share(participants)
        for b in e.get_beneficiaries(participants):
            balances[b] -= share
            
    # Schuldner und Gläubiger trennen
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
            settlements.append({
                "from": debtor_name,
                "to": creditor_name,
                "amount": round(settle_amount, 2)
            })
            
        debtors[i][1] -= settle_amount
        creditors[j][1] -= settle_amount
        
        if debtors[i][1] < 0.01: i += 1
        if creditors[j][1] < 0.01: j += 1
            
    return settlements
