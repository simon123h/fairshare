<template>
  <div class="balance-table card">
    <h2 class="section-title">
      <span class="mdi mdi-chart-bar"></span> {{ t('web.overview') }}
    </h2>

    <div v-if="expenses.length === 0" class="empty-state">
      <p>{{ t('web.noExpenses') }}</p>
    </div>

    <div v-else class="table-container">
      <table class="balances-table">
        <thead>
          <tr>
            <th>{{ t('core.name') }}</th>
            <th>{{ t('core.paid') }}</th>
            <th>{{ t('core.share') }}</th>
            <th>{{ t('core.diff') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="row.name">
            <td class="name-cell">
              <span class="avatar mdi mdi-account"></span>
              <span class="name">{{ row.name }}</span>
            </td>
            <td>{{ formatAmount(row.paid) }}</td>
            <td>{{ formatAmount(row.share) }}</td>
            <td :class="getDiffClass(row.difference)">
              {{ formatDifference(row.difference) }}
            </td>
          </tr>
          <tr class="summary-row">
            <td><strong>{{ t('core.total_spent') }}</strong></td>
            <td colspan="3" class="total-spent-cell">
              <strong>{{ formatAmount(totalSpent) }}</strong>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Expense } from '../models/Expense';
import type { ExpenseData } from '../models/Expense';
import { Ledger } from '../models/Ledger';

const props = defineProps<{
  participants: string[];
  expenses: ExpenseData[];
  currency: string;
}>();

const { t } = useI18n();

// Create Ledger instance and compute stats
const ledgerData = computed(() => {
  if (props.participants.length === 0) {
    return { balances: new Map<string, number>(), totalSpent: 0, shares: new Map<string, number>() };
  }

  const ledger = new Ledger(props.participants);
  let totalSpent = 0;
  
  // Track individual totals paid and individual shares
  const paidMap = new Map<string, number>();
  const shareMap = new Map<string, number>();

  props.participants.forEach(p => {
    paidMap.set(p, 0);
    shareMap.set(p, 0);
  });

  props.expenses.forEach(e => {
    try {
      const exp = new Expense(e);
      ledger.addExpense(exp);
      totalSpent += exp.amount;

      // Add to paid map
      const currentPaid = paidMap.get(exp.payer) ?? 0;
      paidMap.set(exp.payer, currentPaid + exp.amount);

      // Add to share map
      const share = exp.calculateShare(props.participants);
      const beneficiaries = exp.getBeneficiaries(props.participants);
      beneficiaries.forEach(b => {
        const currentShare = shareMap.get(b) ?? 0;
        shareMap.set(b, currentShare + share);
      });
    } catch (err) {
      console.error('Error processing expense for ledger:', err);
    }
  });

  const balances = ledger.calculateBalances();

  return {
    balances,
    totalSpent,
    paidMap,
    shareMap
  };
});

const totalSpent = computed(() => ledgerData.value.totalSpent);

const tableData = computed(() => {
  return props.participants.map(name => {
    const paid = ledgerData.value?.paidMap?.get(name) ?? 0;
    const share = ledgerData.value?.shareMap?.get(name) ?? 0;
    const difference = ledgerData.value?.balances?.get(name) ?? 0;

    return {
      name,
      paid,
      share,
      difference
    };
  });
});

const formatAmount = (val: number) => {
  return `${val.toFixed(2)} ${props.currency}`;
};

const formatDifference = (val: number) => {
  const prefix = val > 0.009 ? '+' : '';
  return `${prefix}${val.toFixed(2)} ${props.currency}`;
};

const getDiffClass = (val: number) => {
  if (val > 0.009) return 'diff-positive';
  if (val < -0.009) return 'diff-negative';
  return 'diff-neutral';
};
</script>

<style scoped>
.balance-table {
  padding: var(--space-4);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0 0 var(--space-4) 0;
}

.empty-state {
  text-align: center;
  padding: var(--space-6);
  color: var(--color-text-secondary);
}

.table-container {
  overflow-x: auto;
}

.balances-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.balances-table th,
.balances-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
}

.balances-table th {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.name-cell {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.avatar {
  font-size: 1.1em;
}

.name {
  font-weight: var(--font-weight-medium);
}

.diff-positive {
  color: var(--color-success);
  font-weight: var(--font-weight-semibold);
}

.diff-negative {
  color: var(--color-danger);
  font-weight: var(--font-weight-semibold);
}

.diff-neutral {
  color: var(--color-text-muted);
}

.summary-row {
  background: var(--color-bg-alt);
}

.summary-row td {
  border-bottom: none;
}

.total-spent-cell {
  color: var(--color-primary-dark);
}
</style>
