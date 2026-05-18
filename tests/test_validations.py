import unittest

from fairshare.expense import Expense
from fairshare.i18n import set_language
from fairshare.ledger import Ledger


class TestValidations(unittest.TestCase):
    def setUp(self) -> None:
        # Für Tests erzwingen wir Deutsch
        set_language("de")

    def test_negative_amount(self) -> None:
        with self.assertRaisesRegex(ValueError, "Ungültiger Betrag"):
            Expense(payer="Alice", amount=-10.0)

    def test_empty_participants(self) -> None:
        with self.assertRaisesRegex(ValueError, "Teilnehmerliste darf nicht leer sein"):
            Ledger([])

    def test_unknown_payer(self) -> None:
        ledger = Ledger(["Alice", "Bob"])
        # Charlie ist nicht in der Liste
        expense = Expense(payer="Charlie", amount=50.0)
        with self.assertRaisesRegex(
            ValueError, "Zahler 'Charlie' ist nicht in der Teilnehmerliste"
        ):
            ledger.add_expense(expense)

    def test_unknown_beneficiary(self) -> None:
        ledger = Ledger(["Alice", "Bob"])
        # David ist nicht in der Liste
        expense = Expense(payer="Alice", amount=50.0, split_among=["Alice", "David"])
        with self.assertRaisesRegex(
            ValueError, "Person 'David' .* ist nicht in der Teilnehmerliste"
        ):
            ledger.add_expense(expense)


if __name__ == "__main__":
    unittest.main()
