import unittest
from fairshare.expense import Expense
from fairshare.settlement_logic import calculate_settlements

class TestSettlementLogic(unittest.TestCase):
    def test_simple_even_split(self):
        participants = ["Alice", "Bob"]
        expenses = [Expense(payer="Alice", amount=100.0)]
        # Alice paid 100, both owe 50. Alice net +50, Bob net -50.
        settlements = calculate_settlements(expenses, participants)
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements[0], {"from": "Bob", "to": "Alice", "amount": 50.0})

    def test_already_balanced(self):
        participants = ["Alice", "Bob"]
        expenses = [
            Expense(payer="Alice", amount=50.0),
            Expense(payer="Bob", amount=50.0)
        ]
        settlements = calculate_settlements(expenses, participants)
        self.assertEqual(len(settlements), 0)

    def test_partial_split(self):
        participants = ["Alice", "Bob", "Charlie"]
        expenses = [
            # Lars pays 60 just for Falk and Malte (example from prompt)
            Expense(payer="Alice", amount=60.0, split_among=["Bob", "Charlie"])
        ]
        # Alice +60, Bob -30, Charlie -30
        settlements = calculate_settlements(expenses, participants)
        self.assertEqual(len(settlements), 2)
        
        # Check if both owe Alice 30
        names_from = {s['from'] for s in settlements}
        self.assertIn("Bob", names_from)
        self.assertIn("Charlie", names_from)
        for s in settlements:
            self.assertEqual(s['to'], "Alice")
            self.assertEqual(s['amount'], 30.0)

    def test_complex_scenario(self):
        participants = ["Alice", "Bob", "Charlie", "David"]
        expenses = [
            Expense(payer="Alice", amount=100.0), # 25 each
            Expense(payer="Bob", amount=20.0),   # 5 each
        ]
        # Total 120, 30 each.
        # Alice: 100 - 30 = +70
        # Bob: 20 - 30 = -10
        # Charlie: 0 - 30 = -30
        # David: 0 - 30 = -30
        settlements = calculate_settlements(expenses, participants)
        
        total_settled = sum(s['amount'] for s in settlements)
        self.assertEqual(total_settled, 70.0)
        
        # Verify all debt is to Alice
        for s in settlements:
            self.assertEqual(s['to'], "Alice")

if __name__ == '__main__':
    unittest.main()
