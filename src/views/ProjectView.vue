<template>
  <div v-if="project" class="project-view fade-in">
    <!-- Project Header Bar -->
    <header class="project-header">
      <div class="title-area">
        <h1 class="project-title">{{ project.name }}</h1>
      </div>

      <router-link to="/" class="btn btn-secondary back-link">
        <span class="mdi mdi-arrow-left"></span> {{ t('web.cancel') }}
      </router-link>
    </header>

    <!-- Tab Navigation -->
    <nav class="project-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-btn"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <span :class="['mdi', tab.icon]"></span>
        {{ tab.label }}
      </button>
    </nav>

    <!-- Dashboard Content Layout -->
    <main class="tab-content">
      <!-- Expenses Tab -->
      <div v-if="activeTab === 'expenses'" class="tab-pane fade-in">
        <div class="expenses-section card">
          <div class="section-header">
            <h2 class="section-title"><span class="mdi mdi-cash-multiple"></span> {{ t('core.expenses') }}</h2>
            <button
              class="btn btn-primary btn-sm"
              @click="openExpenseForm(null)"
              :disabled="project.participants.length === 0"
            >
              <span class="mdi mdi-plus"></span> {{ t('web.addExpense') }}
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

      <!-- Settlements Tab -->
      <div v-if="activeTab === 'settlements'" class="tab-pane fade-in settlements-layout">
        <div class="settlements-main">
          <!-- Balance table -->
          <BalanceTable
            :participants="project.participants"
            :expenses="project.expenses"
            :currency="project.currency"
          />
        </div>
        <aside class="settlements-sidebar">
          <!-- Settlement card -->
          <SettlementCard
            :participants="project.participants"
            :expenses="project.expenses"
            :currency="project.currency"
            @settle="onSaveExpense"
          />
        </aside>
      </div>

      <!-- Project Settings Tab -->
      <div v-if="activeTab === 'settings'" class="tab-pane fade-in settings-layout">
        <section class="settings-section">
          <!-- Participant Manager Component -->
          <ParticipantManager
            :participants="project.participants"
            @update:participants="onParticipantsUpdate"
          />
        </section>

        <section class="settings-section">
          <!-- Project Details Card -->
          <div class="card">
            <h2 class="section-title">
              <span class="mdi mdi-information-outline"></span> {{ t('web.details') }}
            </h2>
            <div class="settings-group">
              <label class="settings-label">{{ t('web.currency') }}</label>
              <CurrencySelector
                :modelValue="project.currency"
                @update:modelValue="changeCurrency"
              />
            </div>
          </div>
        </section>
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
import { ref, computed } from 'vue';
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

// Tab Management
const activeTab = ref('settings');
const tabs = computed(() => [
  { id: 'settings', label: t('web.projectSettings'), icon: 'mdi-cog-outline' },
  { id: 'expenses', label: t('web.expenses'), icon: 'mdi-cash-multiple' },
  { id: 'settlements', label: t('web.settlements'), icon: 'mdi-handshake-outline' },
]);

// Expense Modal Form States
const showExpenseForm = ref(false);
const editingExpense = ref<ExpenseData | null>(null);

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
</script>

<style scoped>
.project-view {
  max-width: var(--max-width-lg);
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
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

.project-tabs {
  display: flex;
  gap: var(--space-1);
  border-bottom: 2px solid var(--color-border-light);
  margin-bottom: var(--space-4);
  background: var(--color-bg);
  position: sticky;
  top: 0;
  z-index: 50;
  padding-top: var(--space-2);
}

.tab-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.tab-btn:hover {
  color: var(--color-primary);
  background-color: var(--color-primary-50);
}

.tab-btn.active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.tab-content {
  flex: 1;
}

.tab-pane {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.settlements-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
  align-items: start;
}

.settings-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-6);
  align-items: start;
}

.settings-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.settings-group {
  margin-top: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.settings-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-secondary);
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
  display: flex;
  align-items: center;
  gap: var(--space-2);
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
  .settlements-layout,
  .settings-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .project-tabs {
    overflow-x: auto;
    padding-bottom: 2px;
    -webkit-overflow-scrolling: touch;
  }
  
  .tab-btn {
    padding: var(--space-2) var(--space-4);
    font-size: var(--font-size-sm);
  }
}
</style>
