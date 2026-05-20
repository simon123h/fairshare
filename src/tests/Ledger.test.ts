import { describe, it, expect } from 'vitest';
import { Expense } from '../models/Expense';
import { Ledger } from '../models/Ledger';

describe('Ledger Class tests', () => {
  it('should calculate balance correctly in simple 2-person scenario', () => {
    const ledger = new Ledger(['Alice', 'Bob']);
    
    // Alice paid 100 split among everyone (50 each). Alice gets +50, Bob gets -50.
    ledger.addExpense(
      new Expense({
        id: '1',
        payer: 'Alice',
        amount: 100,
        description: 'Hotel',
        splitAmong: null
      })
    );

    const balances = ledger.calculateBalances();
    expect(balances.get('Alice')).toBeCloseTo(50);
    expect(balances.get('Bob')).toBeCloseTo(-50);

    const settlements = ledger.getSettlements();
    expect(settlements).toHaveLength(1);
    expect(settlements[0]).toEqual({
      from: 'Bob',
      to: 'Alice',
      amount: 50
    });
  });

  it('should calculate balance correctly with custom splits', () => {
    const ledger = new Ledger(['Alice', 'Bob', 'Charlie']);

    // Alice paid 90, split only between Alice and Bob (45 each).
    // Alice gets: 90 - 45 = +45
    // Bob gets: -45
    // Charlie gets: 0
    ledger.addExpense(
      new Expense({
        id: '1',
        payer: 'Alice',
        amount: 90,
        description: 'Lunch',
        splitAmong: ['Alice', 'Bob']
      })
    );

    const balances = ledger.calculateBalances();
    expect(balances.get('Alice')).toBeCloseTo(45);
    expect(balances.get('Bob')).toBeCloseTo(-45);
    expect(balances.get('Charlie')).toBeCloseTo(0);

    const settlements = ledger.getSettlements();
    expect(settlements).toHaveLength(1);
    expect(settlements[0]).toEqual({
      from: 'Bob',
      to: 'Alice',
      amount: 45
    });
  });

  it('should show empty settlements when already balanced', () => {
    const ledger = new Ledger(['Alice', 'Bob']);
    
    // Alice paid 50, Bob paid 50. Balanced!
    ledger.addExpense(
      new Expense({
        id: '1',
        payer: 'Alice',
        amount: 50,
        description: 'Taxis',
        splitAmong: null
      })
    );
    ledger.addExpense(
      new Expense({
        id: '2',
        payer: 'Bob',
        amount: 50,
        description: 'Lunch',
        splitAmong: null
      })
    );

    const settlements = ledger.getSettlements();
    expect(settlements).toHaveLength(0);
  });

  it('should resolve complex 4-person settlements correctly', () => {
    const ledger = new Ledger(['Alice', 'Bob', 'Charlie', 'David']);

    // Alice paid 100 (everyone pays 25).
    // Bob paid 40 (everyone pays 10).
    // Charlie paid 20 (everyone pays 5).
    // David paid 0 (everyone pays 0).
    // Expected net balances:
    // Alice: +100 - 25 - 10 - 5 = +60
    // Bob: +40 - 25 - 10 - 5 = 0
    // Charlie: +20 - 25 - 10 - 5 = -20
    // David: 0 - 25 - 10 - 5 = -40
    ledger.addExpense(
      new Expense({
        id: '1',
        payer: 'Alice',
        amount: 100,
        description: 'Hotel',
        splitAmong: null
      })
    );
    ledger.addExpense(
      new Expense({
        id: '2',
        payer: 'Bob',
        amount: 40,
        description: 'Lunch',
        splitAmong: null
      })
    );
    ledger.addExpense(
      new Expense({
        id: '3',
        payer: 'Charlie',
        amount: 20,
        description: 'Drinks',
        splitAmong: null
      })
    );

    const balances = ledger.calculateBalances();
    expect(balances.get('Alice')).toBeCloseTo(60);
    expect(balances.get('Bob')).toBeCloseTo(0);
    expect(balances.get('Charlie')).toBeCloseTo(-20);
    expect(balances.get('David')).toBeCloseTo(-40);

    const settlements = ledger.getSettlements();
    // David pays 40 to Alice, Charlie pays 20 to Alice.
    expect(settlements).toContainEqual({ from: 'David', to: 'Alice', amount: 40 });
    expect(settlements).toContainEqual({ from: 'Charlie', to: 'Alice', amount: 20 });
    expect(settlements).toHaveLength(2);
  });

  it('should throw validation error when payer is not in ledger participant group', () => {
    const ledger = new Ledger(['Alice', 'Bob']);
    expect(() => {
      ledger.addExpense(
        new Expense({
          id: '1',
          payer: 'Charlie',
          amount: 20,
          description: 'Error',
          splitAmong: null
        })
      );
    }).toThrow();
  });

  it('should throw validation error when beneficiary in splitAmong is not in participant group', () => {
    const ledger = new Ledger(['Alice', 'Bob']);
    expect(() => {
      ledger.addExpense(
        new Expense({
          id: '1',
          payer: 'Alice',
          amount: 20,
          description: 'Error',
          splitAmong: ['Alice', 'Charlie']
        })
      );
    }).toThrow();
  });

  it('should throw error when constructor gets empty participants list', () => {
    expect(() => new Ledger([])).toThrow();
  });

  it('should throw error when constructor gets invalid participant names', () => {
    expect(() => new Ledger(['Alice', ' '])).toThrow();
  });
});
