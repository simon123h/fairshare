/**
 * Represents a single expense in the FairShare system.
 * Encapsulates data and logic for cost splitting.
 */

export interface ExpenseData {
  id: string;
  payer: string;
  amount: number;
  description: string;
  splitAmong: string[] | null;
}

export class Expense implements ExpenseData {
  public readonly id: string;
  public readonly payer: string;
  public readonly amount: number;
  public readonly description: string;
  public readonly splitAmong: string[] | null;

  constructor(data: ExpenseData) {
    if (data.amount < 0) {
      throw new Error(`Invalid amount: ${data.amount}. Amounts cannot be negative.`);
    }

    if (!data.payer || typeof data.payer !== 'string' || data.payer.trim().length === 0) {
      throw new Error('A valid name for the payer must be provided.');
    }

    this.id = data.id;
    this.payer = data.payer;
    this.amount = Number(data.amount);
    this.description = data.description;
    this.splitAmong = data.splitAmong;
  }

  /**
   * Returns the list of people participating in this expense.
   * Falls back to defaultParticipants if splitAmong is not set.
   */
  getBeneficiaries(defaultParticipants: string[]): string[] {
    const beneficiaries = this.splitAmong && this.splitAmong.length > 0
      ? this.splitAmong
      : defaultParticipants;

    if (!beneficiaries || beneficiaries.length === 0) {
      throw new Error(`Expense '${this.description}' has no beneficiaries (participant list empty).`);
    }

    return beneficiaries;
  }

  /**
   * Calculates the amount each beneficiary must pay for this expense.
   */
  calculateShare(defaultParticipants: string[]): number {
    const beneficiaries = this.getBeneficiaries(defaultParticipants);
    return this.amount / beneficiaries.length;
  }

  /**
   * Returns a human-readable summary of the expense.
   */
  toString(currency: string): string {
    let splitInfo = '';
    if (this.splitAmong && this.splitAmong.length > 0) {
      splitInfo = ` (split: ${this.splitAmong.join(', ')})`;
    }

    return `${this.payer} paid ${this.amount.toFixed(2)}${currency} for '${this.description}'${splitInfo}`;
  }

  /**
   * Generates a unique ID using crypto.randomUUID().
   */
  static generateId(): string {
    return crypto.randomUUID();
  }
}
