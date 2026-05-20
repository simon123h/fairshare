import { describe, it, expect } from 'vitest';
import { Expense } from '../models/Expense';

describe('Expense Class tests', () => {
  it('should successfully create a valid expense', () => {
    const expense = new Expense({
      id: 'test-id',
      payer: 'Alice',
      amount: 100,
      description: 'Groceries',
      splitAmong: null
    });

    expect(expense.id).toBe('test-id');
    expect(expense.payer).toBe('Alice');
    expect(expense.amount).toBe(100);
    expect(expense.description).toBe('Groceries');
    expect(expense.splitAmong).toBeNull();
  });

  it('should return default participants if splitAmong is not set', () => {
    const expense = new Expense({
      id: 'test-id',
      payer: 'Alice',
      amount: 90,
      description: 'Dinner',
      splitAmong: null
    });

    const defaults = ['Alice', 'Bob', 'Charlie'];
    const beneficiaries = expense.getBeneficiaries(defaults);
    expect(beneficiaries).toEqual(defaults);
    expect(expense.calculateShare(defaults)).toBe(30);
  });

  it('should return custom splitAmong list if configured', () => {
    const expense = new Expense({
      id: 'test-id',
      payer: 'Alice',
      amount: 90,
      description: 'Beer',
      splitAmong: ['Alice', 'Bob']
    });

    const defaults = ['Alice', 'Bob', 'Charlie'];
    const beneficiaries = expense.getBeneficiaries(defaults);
    expect(beneficiaries).toEqual(['Alice', 'Bob']);
    expect(expense.calculateShare(defaults)).toBe(45);
  });

  it('should throw error on negative amount', () => {
    expect(() => {
      new Expense({
        id: 'test-id',
        payer: 'Alice',
        amount: -5,
        description: 'Error',
        splitAmong: null
      });
    }).toThrow();
  });

  it('should throw error on empty/missing payer', () => {
    expect(() => {
      new Expense({
        id: 'test-id',
        payer: '  ',
        amount: 50,
        description: 'Error',
        splitAmong: null
      });
    }).toThrow();
  });

  it('should generate a unique uuid', () => {
    const id1 = Expense.generateId();
    const id2 = Expense.generateId();
    expect(id1).toBeDefined();
    expect(id1).not.toBe(id2);
  });
});
