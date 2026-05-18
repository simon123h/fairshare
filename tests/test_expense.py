import unittest

from fairshare.expense import Expense
from fairshare.i18n import set_language


class TestExpense(unittest.TestCase):
    def setUp(self) -> None:
        # Für Tests erzwingen wir Deutsch, um die Assertions stabil zu halten
        set_language("de")

    def test_initialization(self) -> None:
        exp = Expense(payer="Alice", amount=100.0, description="Test", split_among=["Alice", "Bob"])
        self.assertEqual(exp.payer, "Alice")
        self.assertEqual(exp.amount, 100.0)
        self.assertEqual(exp.description, "Test")
        self.assertEqual(exp.split_among, ["Alice", "Bob"])

    def test_get_beneficiaries_default(self) -> None:
        exp = Expense(payer="Alice", amount=100.0)
        defaults = ["Alice", "Bob", "Charlie"]
        self.assertEqual(exp.get_beneficiaries(defaults), defaults)

    def test_get_beneficiaries_custom(self) -> None:
        custom = ["Bob", "Charlie"]
        exp = Expense(payer="Alice", amount=100.0, split_among=custom)
        self.assertEqual(exp.get_beneficiaries(["Alice", "Bob", "Charlie"]), custom)

    def test_calculate_share_default(self) -> None:
        exp = Expense(payer="Alice", amount=90.0)
        defaults = ["Alice", "Bob", "Charlie"]
        self.assertEqual(exp.calculate_share(defaults), 30.0)

    def test_calculate_share_custom(self) -> None:
        exp = Expense(payer="Alice", amount=90.0, split_among=["Bob", "Charlie"])
        self.assertEqual(exp.calculate_share(["Alice", "Bob", "Charlie"]), 45.0)

    def test_calculate_share_empty(self) -> None:
        exp = Expense(payer="Alice", amount=90.0)
        with self.assertRaisesRegex(ValueError, "Teilnehmerliste leer"):
            exp.calculate_share([])


if __name__ == "__main__":
    unittest.main()
