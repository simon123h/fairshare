import unittest

from fairshare.expense import Expense
from fairshare.ledger import Ledger


class TestSettlementLogic(unittest.TestCase):
    def test_simple_even_split(self) -> None:
        ledger = Ledger(["Alice", "Bob"])
        ledger.add_expense(Expense(payer="Alice", amount=100.0))
        settlements = ledger.get_settlements()
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements[0], {"from": "Bob", "to": "Alice", "amount": 50.0})

    def test_already_balanced(self) -> None:
        ledger = Ledger(["Alice", "Bob"])
        ledger.add_expense(Expense(payer="Alice", amount=50.0))
        ledger.add_expense(Expense(payer="Bob", amount=50.0))
        settlements = ledger.get_settlements()
        self.assertEqual(len(settlements), 0)

    def test_partial_split(self) -> None:
        ledger = Ledger(["Alice", "Bob", "Charlie"])
        ledger.add_expense(Expense(payer="Alice", amount=60.0, split_among=["Bob", "Charlie"]))
        settlements = ledger.get_settlements()
        self.assertEqual(len(settlements), 2)

        names_from = {s["from"] for s in settlements}
        self.assertIn("Bob", names_from)
        self.assertIn("Charlie", names_from)
        for s in settlements:
            self.assertEqual(s["to"], "Alice")
            self.assertEqual(s["amount"], 30.0)

    def test_complex_scenario(self) -> None:
        ledger = Ledger(["Alice", "Bob", "Charlie", "David"])
        ledger.add_expense(Expense(payer="Alice", amount=100.0))
        ledger.add_expense(Expense(payer="Bob", amount=20.0))
        settlements = ledger.get_settlements()

        total_settled = sum(s["amount"] for s in settlements)
        self.assertEqual(total_settled, 70.0)

        for s in settlements:
            self.assertEqual(s["to"], "Alice")


if __name__ == "__main__":
    unittest.main()
