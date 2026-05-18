import yaml
import sys
from typing import List, Dict

def calculate_settlements(expenses: List[Dict], participants: List[str]) -> List[Dict]:
    """
    Berechnet die minimalen Transaktionen, um Schulden auszugleichen.
    """
    if not participants:
        return []

    total_spent = sum(e['amount'] for e in expenses)
    share_per_person = total_spent / len(participants)
    
    balances = {p: 0.0 for p in participants}
    for e in expenses:
        if e['payer'] not in balances:
            print(f"Warnung: Zahler '{e['payer']}' ist nicht in der Teilnehmerliste!")
            continue
        balances[e['payer']] += e['amount']
    
    for p in balances:
        balances[p] -= share_per_person
        
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
        
        if debtors[i][1] < 0.01:
            i += 1
        if creditors[j][1] < 0.01:
            j += 1
            
    return settlements

def main():
    try:
        with open('costs.yaml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        participants = data.get('participants', [])
        expenses = data.get('expenses', [])
        
        if not participants:
            print("Fehler: Keine Teilnehmer in 'costs.yaml' gefunden.")
            return

        print(f"Teilnehmer: {', '.join(participants)}")
        print("Ausgaben:")
        for e in expenses:
            print(f"  {e['payer']} hat {e['amount']:.2f}€ bezahlt")
        
        total = sum(e['amount'] for e in expenses)
        print(f"\nGesamtausgaben: {total:.2f}€")
        print(f"Anteil pro Person: {total / len(participants):.2f}€\n")
        
        settlements = calculate_settlements(expenses, participants)
        
        if not settlements:
            print("Alles ausgeglichen!")
        else:
            print("Vorgeschlagene Zahlungen zum Ausgleich:")
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
