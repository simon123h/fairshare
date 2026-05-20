/**
 * Manages a group of participants and their expenses.
 * Calculates resulting balances and necessary settlement transactions.
 */

import { Expense } from './Expense';

export interface Settlement {
  from: string;
  to: string;
  amount: number;
}

export class Ledger {
  public readonly participants: string[];
  public readonly expenses: Expense[];

  constructor(participants: string[]) {
    if (!participants || participants.length === 0) {
      throw new Error('Participant list cannot be empty.');
    }

    if (participants.some((p) => !p || typeof p !== 'string' || p.trim().length === 0)) {
      throw new Error('All participant names must be valid strings.');
    }

    this.participants = [...participants];
    this.expenses = [];
  }

  /**
   * Adds a new expense to the ledger.
   * Validates that the payer and beneficiaries are part of the participant group.
   */
  addExpense(expense: Expense): void {
    if (!this.participants.includes(expense.payer)) {
      throw new Error(
        `Payer '${expense.payer}' is not in the participant list [${this.participants.join(', ')}].`
      );
    }

    if (expense.splitAmong) {
      for (const person of expense.splitAmong) {
        if (!this.participants.includes(person)) {
          throw new Error(
            `Person '${person}' (in splitAmong of '${expense.description}') is not in the participant list.`
          );
        }
      }
    }

    this.expenses.push(expense);
  }

  /**
   * Calculates the net balance for each participant.
   * Positive: person is owed money. Negative: person owes money.
   */
  calculateBalances(): Map<string, number> {
    const balances = new Map<string, number>();
    for (const p of this.participants) {
      balances.set(p, 0);
    }

    for (const expense of this.expenses) {
      // Credit to the payer
      const currentPayerBalance = balances.get(expense.payer) ?? 0;
      balances.set(expense.payer, currentPayerBalance + expense.amount);

      // Debit for the beneficiaries
      const share = expense.calculateShare(this.participants);
      const beneficiaries = expense.getBeneficiaries(this.participants);
      for (const b of beneficiaries) {
        const currentBalance = balances.get(b) ?? 0;
        balances.set(b, currentBalance - share);
      }
    }

    return balances;
  }

  /**
   * Determines the minimal transactions to settle all balances.
   * Uses a greedy two-pointer algorithm with a threshold of 0.01.
   */
  getSettlements(): Settlement[] {
    const balances = this.calculateBalances();
    const THRESHOLD = 0.01;

    const debtors: [string, number][] = [];
    const creditors: [string, number][] = [];

    for (const [person, balance] of balances.entries()) {
      if (balance < -THRESHOLD) {
        debtors.push([person, Math.abs(balance)]);
      } else if (balance > THRESHOLD) {
        creditors.push([person, balance]);
      }
    }

    const settlements: Settlement[] = [];
    let i = 0;
    let j = 0;

    while (i < debtors.length && j < creditors.length) {
      const debtorName = debtors[i][0];
      const debtAmount = debtors[i][1];
      const creditorName = creditors[j][0];
      const creditAmount = creditors[j][1];

      const settleAmount = Math.min(debtAmount, creditAmount);

      if (settleAmount > THRESHOLD) {
        settlements.push({
          from: debtorName,
          to: creditorName,
          amount: Math.round(settleAmount * 100) / 100,
        });
      }

      debtors[i][1] -= settleAmount;
      creditors[j][1] -= settleAmount;

      if (debtors[i][1] < THRESHOLD) {
        i++;
      }
      if (creditors[j][1] < THRESHOLD) {
        j++;
      }
    }

    return settlements;
  }
}
