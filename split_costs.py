import yaml
from typing import List, Dict, Optional

class Expense:
    """
    Repräsentiert eine einzelne Ausgabe.
    """
    def __init__(self, payer: str, amount: float, description: str = "Ausgabe", 
                 split_among: Optional[List[str]] = None):
        self.payer = payer
        self.amount = float(amount)
        self.description = description
        self.split_among = split_among

    def get_beneficiaries(self, default_participants: List[str]) -> List[str]:
        """Gibt die Liste der Personen zurück, die sich diese Ausgabe teilen."""
        return self.split_among if self.split_among else default_participants

    def calculate_share(self, default_participants: List[str]) -> float:
        """Berechnet den Anteil pro Kopf für diese Ausgabe."""
        beneficiaries = self.get_beneficiaries(default_participants)
        if not beneficiaries:
            return 0.0
        return self.amount / len(beneficiaries)

    def __str__(self):
        split_info = f" (geteilt unter: {', '.join(self.split_among)})" if self.split_among else ""
        return f"{self.payer} hat {self.amount:.2f}€ für '{self.description}' bezahlt{split_info}"


def calculate_settlements(expenses: List[Expense], participants: List[str]) -> List[Dict]:
    """
    Berechnet die minimalen Transaktionen basierend auf Expense-Objekten.
    """
    # Alle involvierten Personen sammeln
    all_people = set(participants)
    for e in expenses:
        all_people.add(e.payer)
        if e.split_among:
            all_people.update(e.split_among)
            
    balances = {p: 0.0 for p in all_people}
    
    for e in expenses:
        # Dem Zahler gutschreiben
        balances[e.payer] += e.amount
        
        # Den Nutznießern belasten
        share = e.calculate_share(participants)
        beneficiaries = e.get_beneficiaries(participants)
        
        for b in beneficiaries:
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

def main():
    try:
        with open('costs.yaml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        participants = data.get('participants', [])
        expenses_data = data.get('expenses', [])
        
        # Mapping von Dict zu Expense-Objekten
        expenses = [
            Expense(
                payer=e['payer'],
                amount=e['amount'],
                description=e.get('description', 'Ausgabe'),
                split_among=e.get('split_among')
            ) for e in expenses_data
        ]
        
        if not participants and not expenses:
            print("Fehler: Keine Teilnehmer oder Ausgaben in 'costs.yaml' gefunden.")
            return

        print(f"Teilnehmer: {', '.join(participants)}")
        print("Ausgaben:")
        for e in expenses:
            print(f"  {e}")
        
        total = sum(e.amount for e in expenses)
        print(f"\nGesamtausgaben: {total:.2f}€")
        
        settlements = calculate_settlements(expenses, participants)
        
        if not settlements:
            print("\nAlles ausgeglichen!")
        else:
            print("\nVorgeschlagene Zahlungen zum Ausgleich:")
            for s in settlements:
                print(f"  {s['from']} zahlt {s['amount']:.2f}€ an {s['to']}")
                
    except FileNotFoundError:
        print("Fehler: Die Datei 'costs.yaml' wurde nicht gefunden.")
    except yaml.YAMLError as exc:
        print(f"Fehler beim Lesen der YAML-Datei: {exc}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
