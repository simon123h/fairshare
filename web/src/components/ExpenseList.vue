<template>
  <div class="expense-list card">
    <h2 class="section-title">
      <span>💸</span> {{ t('core.expenses') }}
    </h2>

    <div v-if="sortedExpenses.length === 0" class="empty-state">
      <span class="emoji">💰</span>
      <p>{{ t('web.noExpenses') }}</p>
    </div>

    <div v-else class="list-container">
      <!-- Desktop Table View -->
      <table class="desktop-table">
        <thead>
          <tr>
            <th>{{ t('table.payer') }}</th>
            <th>{{ t('table.amount') }}</th>
            <th>{{ t('table.desc') }}</th>
            <th>{{ t('table.split') }}</th>
            <th class="actions-col"></th>
          </tr>
        </thead>
        <TransitionGroup name="list" tag="tbody">
          <tr v-for="expense in sortedExpenses" :key="expense.id" class="expense-row">
            <td class="payer-cell">
              <span class="user-avatar">👤</span>
              <span class="name">{{ expense.payer }}</span>
            </td>
            <td class="amount-cell">{{ formatAmount(expense.amount) }}</td>
            <td class="desc-cell">{{ expense.description }}</td>
            <td>
              <span v-if="!expense.splitAmong" class="split-badge all">
                {{ t('table.all') }}
              </span>
              <span v-else class="split-badge custom" :title="expense.splitAmong.join(', ')">
                {{ expense.splitAmong.length }} {{ t('core.participants').toLowerCase() }}
              </span>
            </td>
            <td class="actions-cell">
              <button
                class="btn btn-ghost btn-icon edit-btn"
                @click="emit('edit', expense)"
                :title="t('web.editExpense')"
              >
                ✏️
              </button>
              <button
                class="btn btn-ghost btn-icon delete-btn"
                @click="confirmDelete(expense)"
                :title="t('web.delete')"
              >
                🗑️
              </button>
            </td>
          </tr>
        </TransitionGroup>
      </table>

      <!-- Mobile Card View -->
      <div class="mobile-cards">
        <TransitionGroup name="list">
          <div v-for="expense in sortedExpenses" :key="expense.id" class="mobile-card card">
            <div class="card-header">
              <div class="payer-info">
                <span class="avatar">👤</span>
                <span class="name">{{ expense.payer }}</span>
              </div>
              <div class="amount">{{ formatAmount(expense.amount) }}</div>
            </div>

            <div class="card-body">
              <p class="description">{{ expense.description }}</p>
              <div class="split-info">
                <span class="label">{{ t('table.split') }}:</span>
                <span v-if="!expense.splitAmong" class="split-badge all">
                  {{ t('table.all') }}
                </span>
                <span v-else class="split-badge custom">
                  {{ expense.splitAmong.join(', ') }}
                </span>
              </div>
            </div>

            <div class="card-actions">
              <button class="btn btn-secondary btn-sm" @click="emit('edit', expense)">
                ✏️ {{ t('web.save') }}
              </button>
              <button class="btn btn-danger btn-sm" @click="confirmDelete(expense)">
                🗑️ {{ t('web.delete') }}
              </button>
            </div>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ExpenseData } from '../models/Expense';

const props = defineProps<{
  expenses: ExpenseData[];
  participants: string[];
  currency: string;
}>();

const emit = defineEmits<{
  (e: 'edit', value: ExpenseData): void;
  (e: 'delete', value: string): void;
}>();

const { t } = useI18n();

// Expenses sorted by newest first
const sortedExpenses = computed(() => {
  return [...props.expenses].reverse();
});

const formatAmount = (val: number) => {
  return `${val.toFixed(2)} ${props.currency}`;
};

const confirmDelete = (expense: ExpenseData) => {
  const confirmed = window.confirm(t('web.deleteConfirm'));
  if (confirmed) {
    emit('delete', expense.id);
  }
};
</script>

<style scoped>
.expense-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-secondary);
}

.empty-state .emoji {
  font-size: 2.5rem;
  margin-bottom: var(--space-2);
}

.list-container {
  width: 100%;
}

/* Desktop Table Styles */
.desktop-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.desktop-table th,
.desktop-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
}

.desktop-table th {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.payer-cell {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.user-avatar {
  font-size: 1.1em;
}

.name {
  font-weight: var(--font-weight-medium);
}

.amount-cell {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
}

.desc-cell {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.split-badge {
  font-size: var(--font-size-xs);
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  font-weight: var(--font-weight-medium);
}

.split-badge.all {
  background: var(--color-success-light);
  color: var(--color-success);
}

.split-badge.custom {
  background: var(--color-primary-100);
  color: var(--color-primary-dark);
}

.actions-col {
  width: 90px;
}

.actions-cell {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-1);
}

.edit-btn:hover {
  color: var(--color-primary);
}

.delete-btn:hover {
  color: var(--color-danger);
}

/* Mobile Layout Styles */
.mobile-cards {
  display: none;
  flex-direction: column;
  gap: var(--space-3);
}

.mobile-card {
  padding: var(--space-3);
  background: var(--color-bg);
  border: 1px solid var(--color-border-light);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-2);
}

.payer-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.card-header .amount {
  font-weight: var(--font-weight-bold);
  color: var(--color-primary-dark);
}

.card-body {
  margin-bottom: var(--space-3);
}

.card-body .description {
  font-size: var(--font-size-sm);
  color: var(--color-text);
  margin: 0 0 var(--space-2) 0;
}

.split-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-2);
}

@media (max-width: 768px) {
  .desktop-table {
    display: none;
  }

  .mobile-cards {
    display: flex;
  }
}
</style>
