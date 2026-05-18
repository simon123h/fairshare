from typing import Dict, List

from .ledger import Ledger


class ReportGenerator:
    """
    Erzeugt einen detaillierten Abrechnungsbericht im Markdown-Format.
    """

    @staticmethod
    def generate_markdown(ledger: Ledger, settlements: List[Dict], output_path: str = "report.md"):
        balances = ledger.calculate_balances()
        total_spent = sum(e.amount for e in ledger.expenses)

        # Hilfsberechnung für bezahlte Beträge pro Person
        paid_amounts = {p: 0.0 for p in balances.keys()}
        for e in ledger.expenses:
            paid_amounts[e.payer] += e.amount

        lines = [
            "## Details der Ausgaben",
            "",
            f"**Gesamtausgaben:** {total_spent:.2f} €",
            "",
            "| Zahler | Betrag | Beschreibung | Geteilt unter |",
            "| :--- | :--- | :--- | :--- |",
        ]

        for e in ledger.expenses:
            beneficiaries = ", ".join(e.split_among) if e.split_among else "Alle"
            lines.append(f"| {e.payer} | {e.amount:.2f} € | {e.description} | {beneficiaries} |")

        lines.extend(
            [
                "",
                "## Bilanzen",
                "",
                "| Name | Bezahlt | Soll-Anteil | Differenz |",
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

        lines.extend(["", "## Vorgeschlagene Ausgleichszahlungen", ""])

        if not settlements:
            lines.append("Es sind keine Zahlungen notwendig. Alle Konten sind ausgeglichen.")
        else:
            lines.append("| Von | An | Betrag |")
            lines.append("| :--- | :--- | :--- |")
            for s in settlements:
                lines.append(f"| {s['from']} | {s['to']} | **{s['amount']:.2f} €** |")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return output_path
