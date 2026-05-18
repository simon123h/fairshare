import yaml
import sys
from typing import List, Dict

def calculate_settlements(expenses: List[Dict], participants: List[str]) -> List[Dict]:
    """
    Berechnet die minimalen Transaktionen, um Schulden auszugleichen.
    Unterstützt jetzt individuelle Aufteilungen pro Ausgabe.
    """
    # Alle involvierten Personen sammeln (Teilnehmer + Zahler/Empfänger aus Ausgaben)
    all_people = set(participants)
    for e in expenses:
        all_people.add(e['payer'])
        if 'split_among' in e:
            all_people.update(e['split_among'])
            
    balances = {p: 0.0 for p in all_people}
    
    for e in expenses:
        payer = e['payer']
        amount = float(e['amount'])
        
        # Wer teilt sich diese Ausgabe? (Standard: alle Teilnehmer)
        beneficiaries = e.get('split_among', participants)
        
        if not beneficiaries:
            continue
            
        # Dem Zahler gutschreiben
        balances[payer] += amount
        
        # Den Empfängern (Nutznießern) belasten
        share = amount / len(beneficiaries)
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
    
    # Gieriger Ausgleichsalgorithmus
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
        
        if not participants and not expenses:
            print("Fehler: Keine Teilnehmer oder Ausgaben in 'costs.yaml' gefunden.")
            return

        print(f"Teilnehmer: {', '.join(participants)}")
        print("Ausgaben:")
        for e in expenses:
            p = e['payer']
            a = float(e['amount'])
            desc = e.get('description', 'Ausgabe')
            
            # Info über spezielle Aufteilung
            split_info = ""
            if 'split_among' in e:
                split_info = f" (geteilt unter: {', '.join(e['split_among'])})"
            
            print(f"  {p} hat {a:.2f}€ für '{desc}' bezahlt{split_info}")
        
        total = sum(float(e['amount']) for e in expenses)
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
        import traceback
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
