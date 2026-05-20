import { reactive, computed, watch } from 'vue';
import type { ExpenseData } from '../models/Expense';

export interface ProjectData {
  id: string;
  name: string;
  currency: string;
  participants: string[];
  expenses: ExpenseData[];
  createdAt: string;
  updatedAt: string;
}

interface State {
  projects: Record<string, ProjectData>;
}

// Load initial state from LocalStorage
const loadState = (): State => {
  try {
    const data = localStorage.getItem('fairshare-projects');
    if (data) {
      return { projects: JSON.parse(data) };
    }
  } catch (e) {
    console.error('Error loading projects from localStorage:', e);
  }
  return { projects: {} };
};

const state = reactive<State>(loadState());

// Watch and persist state changes
watch(
  () => state.projects,
  (newProjects) => {
    localStorage.setItem('fairshare-projects', JSON.stringify(newProjects));
  },
  { deep: true }
);

export function useProjects() {
  const projectsList = computed(() => {
    return Object.values(state.projects).sort(
      (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
    );
  });

  const getProject = (id: string): ProjectData | undefined => {
    return state.projects[id];
  };

  const createProject = (name: string, currency: string): ProjectData => {
    const id = crypto.randomUUID();
    const now = new Date().toISOString();
    const newProject: ProjectData = {
      id,
      name: name.trim(),
      currency: currency.trim() || '€',
      participants: [],
      expenses: [],
      createdAt: now,
      updatedAt: now
    };
    state.projects[id] = newProject;
    return newProject;
  };

  const deleteProject = (id: string): void => {
    delete state.projects[id];
  };

  const updateParticipants = (projectId: string, participants: string[]): void => {
    const project = state.projects[projectId];
    if (project) {
      project.participants = [...participants];
      project.updatedAt = new Date().toISOString();
    }
  };

  const updateCurrency = (projectId: string, currency: string): void => {
    const project = state.projects[projectId];
    if (project) {
      project.currency = currency.trim() || '€';
      project.updatedAt = new Date().toISOString();
    }
  };

  const addExpense = (projectId: string, expense: ExpenseData): void => {
    const project = state.projects[projectId];
    if (project) {
      project.expenses.push(expense);
      project.updatedAt = new Date().toISOString();
    }
  };

  const updateExpense = (
    projectId: string,
    expenseId: string,
    updatedFields: Partial<ExpenseData>
  ): void => {
    const project = state.projects[projectId];
    if (project) {
      const index = project.expenses.findIndex((e) => e.id === expenseId);
      if (index !== -1) {
        project.expenses[index] = {
          ...project.expenses[index],
          ...updatedFields
        };
        project.updatedAt = new Date().toISOString();
      }
    }
  };

  const removeExpense = (projectId: string, expenseId: string): void => {
    const project = state.projects[projectId];
    if (project) {
      project.expenses = project.expenses.filter((e) => e.id !== expenseId);
      project.updatedAt = new Date().toISOString();
    }
  };

  return {
    projects: projectsList,
    getProject,
    createProject,
    deleteProject,
    updateParticipants,
    updateCurrency,
    addExpense,
    updateExpense,
    removeExpense
  };
}
