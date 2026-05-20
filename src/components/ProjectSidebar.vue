<template>
  <div>
    <!-- Backdrop for Mobile -->
    <div
      v-if="isOpen"
      class="sidebar-backdrop"
      @click="emit('close')"
    ></div>

    <!-- Sidebar Container -->
    <aside class="project-sidebar" :class="{ 'mobile-open': isOpen }">
      <div class="sidebar-header">
        <button
          v-if="!showNewForm"
          class="btn btn-primary w-full add-project-btn"
          @click="showNewForm = true"
        >
          <span class="mdi mdi-plus"></span> {{ t('web.newProject') }}
        </button>

        <!-- New Project Form -->
        <Transition name="slide">
          <form v-if="showNewForm" @submit.prevent="handleCreate" class="new-project-form card">
            <h3 class="form-title">{{ t('web.newProject') }}</h3>
            
            <div class="form-group">
              <label for="new-project-name" class="sr-only">{{ t('web.projectName') }}</label>
              <input
                id="new-project-name"
                ref="nameInputRef"
                type="text"
                v-model="newProjectName"
                :placeholder="t('web.projectName')"
                class="form-control"
                required
              />
            </div>

            <div class="form-group">
              <span class="label-text">{{ t('web.currency') }}</span>
              <CurrencySelector v-model="newProjectCurrency" />
            </div>

            <div class="form-actions">
              <button
                type="button"
                class="btn btn-ghost btn-sm"
                @click="cancelCreate"
              >
                {{ t('web.cancel') }}
              </button>
              <button
                type="submit"
                class="btn btn-primary btn-sm"
                :disabled="!newProjectName.trim()"
              >
                {{ t('web.createProject') }}
              </button>
            </div>
          </form>
        </Transition>
      </div>

      <!-- Projects List -->
      <div class="projects-list-container">
        <div v-if="projects.length === 0" class="empty-state">
           <span class="emoji mdi mdi-folder-outline" style="font-size: 2.5rem; display: block; margin-bottom: 8px;"></span>
          <p>{{ t('web.noProjects') }}</p>
        </div>

        <ul v-else class="projects-list">
          <li
            v-for="project in projects"
            :key="project.id"
            class="project-item"
            :class="{ active: route.params.id === project.id }"
            @click="selectProject(project.id)"
          >
            <div class="project-info">
              <span class="project-name">{{ project.name }}</span>
              <div class="project-meta">
                <span class="badge participants-badge">
                   <span class="mdi mdi-account-group"></span> {{ project.participants.length }}
                </span>
                <span class="badge currency-badge">
                  {{ project.currency }}
                </span>
              </div>
            </div>

            <button
              class="btn btn-ghost btn-icon delete-btn"
              @click.stop="handleDelete(project)"
              :title="t('web.deleteProject')"
            >
               <span class="mdi mdi-delete-outline"></span>
            </button>
          </li>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useProjects } from '../composables/useProjects';
import type { ProjectData } from '../composables/useProjects';
import CurrencySelector from './CurrencySelector.vue';

defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: 'close'): void;
}>();

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const { projects, createProject, deleteProject } = useProjects();

const showNewForm = ref(false);
const newProjectName = ref('');
const newProjectCurrency = ref('€');
const nameInputRef = ref<HTMLInputElement | null>(null);

watch(showNewForm, async (val) => {
  if (val) {
    await nextTick();
    nameInputRef.value?.focus();
  }
});

const handleCreate = () => {
  if (!newProjectName.value.trim()) return;
  const project = createProject(newProjectName.value, newProjectCurrency.value);
  newProjectName.value = '';
  newProjectCurrency.value = '€';
  showNewForm.value = false;
  
  router.push({ name: 'project', params: { id: project.id } });
  emit('close');
};

const cancelCreate = () => {
  showNewForm.value = false;
  newProjectName.value = '';
  newProjectCurrency.value = '€';
};

const selectProject = (id: string) => {
  router.push({ name: 'project', params: { id } });
  emit('close');
};

const handleDelete = (project: ProjectData) => {
  const confirmed = window.confirm(t('web.deleteConfirm'));
  if (confirmed) {
    deleteProject(project.id);
    if (route.params.id === project.id) {
      router.push({ name: 'home' });
    }
  }
};
</script>

<style scoped>
.sidebar-backdrop {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-overlay);
  backdrop-filter: blur(4px);
  z-index: calc(var(--z-sticky) - 2);
  display: none;
}

.project-sidebar {
  width: 280px;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px);
  position: sticky;
  top: 64px;
  transition: transform var(--transition-normal);
  z-index: calc(var(--z-sticky) - 1);
}

.sidebar-header {
  padding: var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
}

.add-project-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

.new-project-form {
  padding: var(--space-3);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
}

.form-title {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-2);
}

.form-group {
  margin-bottom: var(--space-3);
}

.label-text {
  display: block;
  font-size: var(--font-size-xs);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
}

.projects-list-container {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-2) 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  text-align: center;
  color: var(--color-text-muted);
}

.empty-state .emoji {
  font-size: 2rem;
  margin-bottom: var(--space-2);
}

.projects-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.project-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-3) var(--space-4);
  cursor: pointer;
  transition: all var(--transition-fast);
  border-left: 3px solid transparent;
}

.project-item:hover {
  background: var(--color-surface-hover);
}

.project-item.active {
  background: var(--color-primary-50);
  border-left-color: var(--color-primary);
}

.project-item.active .project-name {
  color: var(--color-primary);
  font-weight: var(--font-weight-semibold);
}

.project-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.project-name {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.project-meta {
  display: flex;
  gap: var(--space-2);
}

.badge {
  font-size: var(--font-size-xs);
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
}

.participants-badge {
  background: var(--color-border-light);
  color: var(--color-text-secondary);
}

.currency-badge {
  background: var(--color-primary-100);
  color: var(--color-primary-dark);
}

.delete-btn {
  opacity: 0;
  color: var(--color-text-muted);
  transition: opacity var(--transition-fast);
  padding: var(--space-1);
}

.project-item:hover .delete-btn {
  opacity: 1;
}

.delete-btn:hover {
  color: var(--color-danger);
}

@media (max-width: 768px) {
  .sidebar-backdrop {
    display: block;
  }

  .project-sidebar {
    position: fixed;
    transform: translateX(-100%);
    box-shadow: var(--shadow-xl);
  }

  .project-sidebar.mobile-open {
    transform: translateX(0);
  }
}
</style>
