<template>
  <div class="home-view fade-in">
    <!-- Hero Banner -->
    <header class="hero-section text-center">
      <h1 class="display-title">{{ t('web.title') }}</h1>
      <p class="subtitle">{{ t('web.subtitle') }}</p>
    </header>

    <!-- Content Area -->
    <main class="content-container">
      <div v-if="projects.length === 0" class="empty-dashboard card text-center scale-in">
        <div class="empty-illustration mdi mdi-piggy-bank-outline" style="font-size: 3.5rem; color: var(--color-primary-300); margin-bottom: var(--space-4);"></div>
        <h2>{{ t('web.noProjects') }}</h2>
        <p>{{ t('web.getStarted') }}</p>
      </div>

      <div v-else class="dashboard-grid">
        <h2 class="grid-title w-full">{{ t('tui.select_project') }}</h2>
        <div
          v-for="project in projects"
          :key="project.id"
          class="project-card card hover-lift"
          @click="openProject(project.id)"
        >
          <div class="card-header">
            <h3 class="project-name">{{ project.name }}</h3>
            <span class="currency-badge">{{ project.currency }}</span>
          </div>

          <div class="card-stats">
            <div class="stat-item">
              <span class="stat-icon mdi mdi-account-group"></span>
              <span class="stat-text">
                {{ project.participants.length }} {{ t('core.participants').toLowerCase() }}
              </span>
            </div>
            <div class="stat-item">
              <span class="stat-icon mdi mdi-cash-multiple"></span>
              <span class="stat-text">
                {{ project.expenses.length }} {{ t('core.expenses').toLowerCase() }}
              </span>
            </div>
          </div>

          <footer class="card-footer">
            <span class="updated-at">
              <span class="mdi mdi-clock-outline"></span> {{ formatRelativeTime(project.updatedAt) }}
            </span>
          </footer>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useProjects } from '../composables/useProjects';

const router = useRouter();
const { t, locale } = useI18n();
const { projects } = useProjects();

const openProject = (id: string) => {
  router.push({ name: 'project', params: { id } });
};

// Formats absolute ISO string to relative string representation
const formatRelativeTime = (isoString: string): string => {
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 600);

  // Localized date formatting for general fallback
  const dtf = new Intl.DateTimeFormat(locale.value, {
    dateStyle: 'medium',
    timeStyle: 'short'
  });

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${Math.floor(diffMins / 60)}h ago`;
  
  return dtf.format(date);
};
</script>

<style scoped>
.home-view {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.hero-section {
  padding: var(--space-4) 0;
}

.display-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--space-2);
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: var(--font-size-md);
  color: var(--color-text-secondary);
}

.content-container {
  display: flex;
  justify-content: center;
}

.empty-dashboard {
  max-width: 500px;
  width: 100%;
  padding: var(--space-8);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
}

.empty-illustration {
  font-size: 3.5rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
  width: 100%;
}

.grid-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-2);
  color: var(--color-text);
}

.project-card {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  cursor: pointer;
  background: var(--color-surface);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-2);
}

.project-name {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0;
  color: var(--color-text);
  line-height: var(--line-height-tight);
}

.currency-badge {
  background: var(--color-primary-100);
  color: var(--color-primary-dark);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
}

.card-stats {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.card-footer {
  border-top: 1px solid var(--color-border-light);
  padding-top: var(--space-2);
  margin-top: auto;
}

.updated-at {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
}

.text-center {
  text-align: center;
}

.w-full {
  grid-column: 1 / -1;
}
</style>
