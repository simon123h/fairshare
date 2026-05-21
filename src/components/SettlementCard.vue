<template>
  <div class="settlements-section card">
    <h2 class="section-title">
      <span class="mdi mdi-handshake-outline"></span> {{ t('web.settlements') }}
    </h2>

    <div v-if="expenses.length === 0" class="empty-state">
      <p>{{ t('web.noExpenses') }}</p>
    </div>

    <div v-else-if="settlements.length === 0" class="settled-state bounce-in">
      <span class="checkmark mdi mdi-check-circle-outline" style="font-size: 2.5rem; color: var(--color-success); display: block; margin-bottom: 8px;"></span>
      <p class="settled-text">{{ t('web.allSettled') }}</p>
    </div>

    <div v-else class="settlements-list">
      <div
        v-for="(settlement, index) in settlements"
        :key="index"
        class="settlement-card"
      >
        <div class="settlement-info">
          <div class="person debtor">
            <span class="avatar mdi mdi-account"></span>
            <span class="name">{{ settlement.from }}</span>
          </div>

          <div class="arrow-container">
            <span class="amount-badge">{{ formatAmount(settlement.amount) }}</span>
            <div class="animated-arrow">
              <div class="line"></div>
              <div class="point"></div>
            </div>
          </div>

          <div class="person creditor">
            <span class="avatar mdi mdi-account"></span>
            <span class="name">{{ settlement.to }}</span>
          </div>

          <!-- Settle Button -->
          <div class="action-area">
            <button
              class="btn btn-ghost btn-icon settle-btn"
              @click="onSettle(settlement)"
              :title="t('web.recordSettlement')"
            >
              <span class="mdi mdi-check"></span>
            </button>
          </div>
        </div>

        <p class="description-text">
          {{ t('web.paysTo', { from: settlement.from, amount: formatAmount(settlement.amount), to: settlement.to }) }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { Expense } from '../models/Expense';
import type { ExpenseData } from '../models/Expense';
import { Ledger } from '../models/Ledger';
import type { Settlement } from '../models/Ledger';

const props = defineProps<{
  participants: string[];
  expenses: ExpenseData[];
  currency: string;
}>();

const emit = defineEmits<{
  (e: 'settle', value: ExpenseData): void;
}>();

const { t } = useI18n();

const settlements = computed<Settlement[]>(() => {
  if (props.participants.length === 0) return [];
  const ledger = new Ledger(props.participants);
  
  props.expenses.forEach(e => {
    try {
      ledger.addExpense(new Expense(e));
    } catch (err) {
      console.error(err);
    }
  });

  return ledger.getSettlements();
});

const onSettle = (settlement: Settlement) => {
  const expense: ExpenseData = {
    id: Expense.generateId(),
    payer: settlement.from,
    amount: settlement.amount,
    description: t('web.settlementDesc', { from: settlement.from, to: settlement.to }),
    splitAmong: [settlement.to]
  };
  emit('settle', expense);
};

const formatAmount = (val: number) => {
  return `${val.toFixed(2)} ${props.currency}`;
};
</script>

<style scoped>
.settlements-section {
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

.settled-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  text-align: center;
}

.checkmark {
  font-size: 2.5rem;
  margin-bottom: var(--space-2);
}

.settled-text {
  font-weight: var(--font-weight-medium);
  color: var(--color-success);
}

.settlements-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.settlement-card {
  background: var(--color-bg);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: var(--space-2) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.settlement-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.person {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--space-2);
  flex: 1;
  min-width: 0;
}

.person .avatar {
  font-size: 1.125rem;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.person .name {
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.person.creditor {
  flex-direction: row-reverse;
}

.person.creditor .name {
  text-align: right;
}

.arrow-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 0 0 80px;
  gap: var(--space-1);
}

.amount-badge {
  background: var(--color-primary-100);
  color: var(--color-primary-dark);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-xs);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
}

.animated-arrow {
  display: flex;
  align-items: center;
  width: 100%;
  position: relative;
  height: 4px;
}

.animated-arrow .line {
  height: 2px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  flex: 1;
}

.animated-arrow .point {
  width: 0;
  height: 0;
  border-top: 4px solid transparent;
  border-bottom: 4px solid transparent;
  border-left: 6px solid var(--color-accent);
}

.action-area {
  display: flex;
  align-items: center;
  margin-left: var(--space-2);
}

.settle-btn {
  color: var(--color-success);
  opacity: 0.6;
}

.settle-btn:hover {
  opacity: 1;
  background-color: var(--color-success-light);
  color: var(--color-success);
}

.description-text {
  display: none;
}
</style>
