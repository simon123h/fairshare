import unittest

from fairshare.i18n import _, set_language


class TestI18n(unittest.TestCase):
    def test_lithuanian(self):
        set_language("lt")
        self.assertEqual(_("core.participants"), "Dalyviai")
        self.assertEqual(_("core.expenses"), "Išlaidos")
        self.assertEqual(
            _("core.pays_to", from_p="A", amount=10, to_p="B"), "A moka 10.00€ asmeniui B"
        )

    def test_japanese(self):
        set_language("ja")
        self.assertEqual(_("core.participants"), "参加者")
        self.assertEqual(_("core.expenses"), "経費")
        self.assertEqual(
            _("core.pays_to", from_p="A", amount=10, to_p="B"), "A が B に 10.00€ 支払います"
        )

    def test_chinese(self):
        set_language("zh")
        self.assertEqual(_("core.participants"), "参与者")
        self.assertEqual(_("core.expenses"), "费用")
        self.assertEqual(_("core.pays_to", from_p="A", amount=10, to_p="B"), "A 向 B 支付 10.00€")


if __name__ == "__main__":
    unittest.main()
