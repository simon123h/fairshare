import yaml
from expense import Expense
from settlement_logic import calculate_settlements

def main():
    try:
        with open('costs.yaml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            
        participants = data.get('participants', [])
        expenses_data = data.get('expenses', [])
        
        # Umwandlung der YAML-Daten in Expense-Objekte
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
            print(f"  {e}") # Nutzt die __str__ Methode der Klasse
        
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
