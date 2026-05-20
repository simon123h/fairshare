<template>
  <div class="modal-overlay" @click.self="cancel">
    <div class="modal-card card scale-in" role="dialog" aria-modal="true">
      <header class="modal-header">
        <h2 class="modal-title">
          {{ expense ? t('web.editExpense') : t('web.addExpense') }}
        </h2>
        <button class="btn btn-ghost btn-icon close-btn" @click="cancel">✕</button>
      </header>

      <form @submit.prevent="submit" class="modal-body">
        <!-- Payer selection -->
        <div class="form-group">
          <label for="expense-payer" class="form-label">{{ t('web.payer') }}</label>
          <select
            id="expense-payer"
            ref="firstInputRef"
            v-model="payer"
            class="form-control"
            required
          >
            <option value="" disabled>{{ t('web.payer') }}</option>
            <option v-for="person in participants" :key="person" :value="person">
              {{ person }}
            </option>
          </select>
        </div>

        <!-- Amount and description -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label for="expense-amount" class="form-label">{{ t('web.amount') }}</label>
            <div class="input-addon-group">
              <input
                id="expense-amount"
                type="number"
                step="0.01"
                min="0.01"
                v-model.number="amount"
                class="form-control"
                required
              />
              <span class="addon">{{ currency }}</span>
            </div>
          </div>

          <div class="form-group flex-2">
            <label for="expense-desc" class="form-label">{{ t('web.description') }}</label>
            <input
              id="expense-desc"
              type="text"
              v-model="description"
              :placeholder="t('web.descriptionPlaceholder')"
              class="form-control"
            />
          </div>
        </div>

        <!-- Split Options -->
        <div class="form-group">
          <label class="form-label">{{ t('wizard.split.q') }}</label>
          <div class="radio-group">
            <label class="radio-option" :class="{ active: splitType === 'all' }">
              <input type="radio" value="all" v-model="splitType" />
              <span>{{ t('web.splitAll') }}</span>
            </label>
            <label class="radio-option" :class="{ active: splitType === 'custom' }">
              <input type="radio" value="custom" v-model="splitType" />
              <span>{{ t('web.splitCustom') }}</span>
            </label>
          </div>
        </div>

        <!-- Custom split checkboxes -->
        <Transition name="slide">
          <div v-if="splitType === 'custom'" class="custom-split-list card">
            <span class="instruction-text">{{ t('wizard.checkbox.q') }}</span>
            <div class="checkbox-grid">
              <label
                v-for="person in participants"
                :key="person"
                class="checkbox-label"
              >
                <input
                  type="checkbox"
                  :value="person"
                  :checked="splitAmong.includes(person)"
                  @change="togglePerson(person)"
                />
                <span>{{ person }}</span>
              </label>
            </div>
          </div>
        </Transition>

        <footer class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="cancel">
            {{ t('web.cancel') }}
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!isValid"
          >
            {{ t('web.save') }}
          </button>
        </footer>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { Expense } from '../models/Expense';
import type { ExpenseData } from '../models/Expense';

const props = defineProps<{
  participants: string[];
  currency: string;
  expense?: ExpenseData | null;
}>();

const emit = defineEmits<{
  (e: 'save', value: ExpenseData): void;
  (e: 'cancel'): void;
}>();

const { t } = useI18n();

const payer = ref('');
const amount = ref<number | ''>('');
const description = ref('');
const splitType = ref<'all' | 'custom'>('all');
const splitAmong = ref<string[]>([]);
const firstInputRef = ref<HTMLSelectElement | null>(null);

// Populate fields on edit
if (props.expense) {
  payer.value = props.expense.payer;
  amount.value = props.expense.amount;
  description.value = props.expense.description;
  if (props.expense.splitAmong && props.expense.splitAmong.length > 0) {
    splitType.value = 'custom';
    splitAmong.value = [...props.expense.splitAmong];
  } else {
    splitType.value = 'all';
    splitAmong.value = [];
  }
}

const togglePerson = (person: string) => {
  if (splitAmong.value.includes(person)) {
    splitAmong.value = splitAmong.value.filter(p => p !== person);
  } else {
    splitAmong.value = [...splitAmong.value, person];
  }
};

const isValid = computed(() => {
  const isPayerValid = payer.value !== '';
  const isAmountValid = typeof amount.value === 'number' && amount.value > 0;
  const isSplitValid =
    splitType.value === 'all' ||
    (splitType.value === 'custom' && splitAmong.value.length > 0);

  return isPayerValid && isAmountValid && isSplitValid;
});

const submit = () => {
  if (!isValid.value) return;

  const id = props.expense ? props.expense.id : Expense.generateId();
  const finalizedSplitAmong = splitType.value === 'custom' ? splitAmong.value : null;

  const data: ExpenseData = {
    id,
    payer: payer.value,
    amount: amount.value as number,
    description: description.value.trim() || t('table.desc'),
    splitAmong: finalizedSplitAmong
  };

  emit('save', data);
};

const cancel = () => {
  emit('cancel');
};

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    cancel();
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
  firstInputRef.value?.focus();
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-overlay);
  backdrop-filter: blur(4px);
  z-index: var(--z-modal);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--space-4);
}

.modal-card {
  width: 100%;
  max-width: 500px;
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
}

.modal-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0;
}

.close-btn {
  font-size: 1.1em;
  padding: var(--space-1);
}

.modal-body {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.form-row {
  display: flex;
  gap: var(--space-4);
}

.flex-1 {
  flex: 1;
}

.flex-2 {
  flex: 2;
}

.form-label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  margin-bottom: var(--space-1);
}

.input-addon-group {
  display: flex;
  align-items: stretch;
}

.input-addon-group .form-control {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-right: none;
}

.addon {
  display: flex;
  align-items: center;
  padding: 0 var(--space-3);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-left: none;
  border-top-right-radius: var(--radius-md);
  border-bottom-right-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: all var(--transition-fast);
}

.radio-option:hover {
  background-color: var(--color-bg-alt);
  border-color: var(--color-text-muted);
}

.radio-option.active {
  background-color: var(--color-primary-50);
  border-color: var(--color-primary);
  color: var(--color-primary-dark);
}

.radio-option input[type="radio"] {
  accent-color: var(--color-primary);
  width: 16px;
  height: 16px;
}

.custom-split-list {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  padding: var(--space-3);
}

.instruction-text {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2);
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: var(--space-2);
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  font-size: var(--font-size-sm);
}

.checkbox-label input[type="checkbox"] {
  accent-color: var(--color-primary);
  width: 16px;
  height: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  margin-top: var(--space-2);
}
</style>
