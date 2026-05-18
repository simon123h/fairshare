from typing import Any, Dict, List

from .i18n import _
from .ledger import Ledger


class ReportGenerator:
    """
    Erzeugt einen detaillierten Abrechnungsbericht im Markdown-Format.
    Layout angepasst an die manuellen Änderungen des Users.
    """

    @staticmethod
    def generate_markdown(
        ledger: Ledger, settlements: List[Dict[str, Any]], output_path: str = "report.md"
    ) -> str:
        balances = ledger.calculate_balances()
        total_spent = sum(e.amount for e in ledger.expenses)

        # Hilfsberechnung für bezahlte Beträge pro Person
        paid_amounts = {p: 0.0 for p in balances.keys()}
        for e in ledger.expenses:
            paid_amounts[e.payer] += e.amount

        # Tabellen-Header übersetzen
        payer_l = _("table.payer")
        amount_l = _("table.amount")
        desc_l = _("table.desc")
        split_l = _("table.split")

        lines = [
            f"## {_('report.details')}",
            "",
            f"**{_('core.total_spent')}:** {total_spent:.2f} €",
            "",
            f"| {payer_l} | {amount_l} | {desc_l} | {split_l} |",
            "| :--- | :--- | :--- | :--- |",
        ]

        for e in ledger.expenses:
            beneficiaries = ", ".join(e.split_among) if e.split_among else _("table.all")
            lines.append(f"| {e.payer} | {e.amount:.2f} € | {e.description} | {beneficiaries} |")

        lines.extend(
            [
                "",
                f"## {_('report.balances')}",
                "",
                f"| {_('core.name')} | {_('core.paid')} | {_('core.share')} | {_('core.diff')} |",
                "| :--- | :------: | :---------: | :---------: |",
            ]
        )

        for person in sorted(balances.keys()):
            paid = paid_amounts[person]
            diff = balances[person]
            share = paid - diff
            status = "+" if diff > 0.005 else "-" if diff < -0.005 else ""
            lines.append(
                f"| {person} | {paid:.2f} € | {share:.2f} € | **{status}{abs(diff):.2f} €** |"
            )

        lines.extend(["", f"## {_('report.settlements')}", ""])

        if not settlements:
            lines.append(_("report.no_settlements"))
        else:
            lines.append(f"| {_('table.from')} | {_('table.to')} | {_('table.amount')} |")
            lines.append("| :--- | :--- | :--- |")
            for s in settlements:
                lines.append(f"| {s['from']} | {s['to']} | **{s['amount']:.2f} €** |")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return output_path
