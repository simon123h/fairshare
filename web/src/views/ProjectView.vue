<template>
  <div v-if="project" class="project-view fade-in">
    <!-- Project Header Bar -->
    <header class="project-header">
      <div class="title-area">
        <h1 class="project-title">{{ project.name }}</h1>
        
        <!-- Interactive Currency Badge -->
        <div class="currency-badge-container" ref="currencyDropdownRef">
          <button
            class="currency-badge hover-lift"
            @click="toggleCurrencyDropdown"
            :title="t('web.currency')"
          >
            <span>{{ project.currency }}</span>
            <span class="edit-icon">✏️</span>
          </button>

          <!-- Inline Currency Switcher -->
          <Transition name="fade">
            <div v-if="showCurrencyDropdown" class="currency-dropdown card shadow-lg">
              <h4 class="dropdown-title">{{ t('web.currency') }}</h4>
              <CurrencySelector
                :modelValue="project.currency"
                @update:modelValue="changeCurrency"
              />
            </div>
          </Transition>
        </div>
      </div>

      <router-link to="/" class="btn btn-secondary btn-sm back-link">
        ← {{ t('web.cancel') }}
      </router-link>
    </header>

    <!-- Dashboard Content Layout -->
    <main class="project-layout">
      <!-- Left Column: Participants and Transactions -->
      <div class="layout-main">
        <!-- Participant Manager Component -->
        <ParticipantManager
          :participants="project.participants"
          :currency="project.currency"
          @update:participants="onParticipantsUpdate"
        />

        <!-- Expense Recorder -->
        <div class="expenses-section card">
          <div class="section-header">
            <h2 class="section-title">💸 {{ t('core.expenses') }}</h2>
            <button
              class="btn btn-primary btn-sm"
              @click="openExpenseForm(null)"
              :disabled="project.participants.length === 0"
            >
              ＋ {{ t('web.addExpense') }}
            </button>
          </div>

          <ExpenseList
            :expenses="project.expenses"
            :participants="project.participants"
            :currency="project.currency"
            @edit="openExpenseForm"
            @delete="onDeleteExpense"
          />
        </div>
      </div>

      <!-- Right Column: Balance overview and settlements calculation -->
      <div class="layout-sidebar">
        <!-- Balance table -->
        <BalanceTable
          :participants="project.participants"
          :expenses="project.expenses"
          :currency="project.currency"
        />

        <!-- Settlement card -->
        <SettlementCard
          :participants="project.participants"
          :expenses="project.expenses"
          :currency="project.currency"
        />
      </div>
    </main>

    <!-- Expense Modal Form -->
    <ExpenseForm
      v-if="showExpenseForm"
      :participants="project.participants"
      :currency="project.currency"
      :expense="editingExpense"
      @save="onSaveExpense"
      @cancel="closeExpenseForm"
    />
  </div>

  <!-- Project Not Found -->
  <div v-else class="project-not-found card text-center scale-in">
    <h2>404</h2>
    <p>Project not found.</p>
    <router-link to="/" class="btn btn-primary">
      Go back home
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useProjects } from '../composables/useProjects';
import type { ExpenseData } from '../models/Expense';
import ParticipantManager from '../components/ParticipantManager.vue';
import ExpenseList from '../components/ExpenseList.vue';
import BalanceTable from '../components/BalanceTable.vue';
import SettlementCard from '../components/SettlementCard.vue';
import ExpenseForm from '../components/ExpenseForm.vue';
import CurrencySelector from '../components/CurrencySelector.vue';

const route = useRoute();
const { t } = useI18n();
const {
  getProject,
  updateParticipants,
  updateCurrency,
  addExpense,
  updateExpense,
  removeExpense
} = useProjects();

const projectId = computed(() => route.params.id as string);
const project = computed(() => getProject(projectId.value));

// Currency Editing State
const showCurrencyDropdown = ref(false);
const currencyDropdownRef = ref<HTMLElement | null>(null);

// Expense Modal Form States
const showExpenseForm = ref(false);
const editingExpense = ref<ExpenseData | null>(null);

const toggleCurrencyDropdown = () => {
  showCurrencyDropdown.value = !showCurrencyDropdown.value;
};

const changeCurrency = (symbol: string) => {
  if (project.value && symbol) {
    updateCurrency(project.value.id, symbol);
  }
};

const onParticipantsUpdate = (newParticipants: string[]) => {
  if (project.value) {
    updateParticipants(project.value.id, newParticipants);
  }
};

const openExpenseForm = (expense: ExpenseData | null) => {
  editingExpense.value = expense;
  showExpenseForm.value = true;
};

const closeExpenseForm = () => {
  showExpenseForm.value = false;
  editingExpense.value = null;
};

const onSaveExpense = (expense: ExpenseData) => {
  if (!project.value) return;

  if (editingExpense.value) {
    updateExpense(project.value.id, expense.id, expense);
  } else {
    addExpense(project.value.id, expense);
  }
  closeExpenseForm();
};

const onDeleteExpense = (expenseId: string) => {
  if (project.value) {
    removeExpense(project.value.id, expenseId);
  }
};

// Outside click handling for currency switcher
const handleClickOutside = (event: MouseEvent) => {
  if (
    currencyDropdownRef.value &&
    !currencyDropdownRef.value.contains(event.target as Node)
  ) {
    showCurrencyDropdown.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

// Close dropdown on route change
watch(projectId, () => {
  showCurrencyDropdown.value = false;
});
</script>

<style scoped>
.project-view {
  max-width: var(--max-width-lg);
  margin: 0 auto;
  padding: var(--space-6) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--space-4);
}

.title-area {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.project-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  margin: 0;
  color: var(--color-text);
}

.currency-badge-container {
  position: relative;
}

.currency-badge {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  background: var(--color-primary-100);
  color: var(--color-primary-dark);
  font-weight: var(--font-weight-bold);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  border: 1px solid transparent;
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: all var(--transition-fast);
}

.currency-badge:hover {
  background: var(--color-primary-200);
  border-color: var(--color-primary-dark);
}

.currency-badge .edit-icon {
  font-size: 0.8em;
  opacity: 0.7;
}

.currency-dropdown {
  position: absolute;
  top: 110%;
  left: 0;
  z-index: var(--z-dropdown);
  min-width: 250px;
  padding: var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
}

.dropdown-title {
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  margin: 0 0 var(--space-2) 0;
  color: var(--color-text-secondary);
}

.project-layout {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--space-6);
  align-items: start;
}

.layout-main,
.layout-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.expenses-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0;
}

.back-link {
  text-decoration: none;
}

.project-not-found {
  max-width: 400px;
  margin: var(--space-16) auto;
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
}

@media (max-width: 1024px) {
  .project-layout {
    grid-template-columns: 1fr;
  }
}
</style>
