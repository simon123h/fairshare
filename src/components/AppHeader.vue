<template>
  <header class="app-header glass">
    <div class="header-container">
      <div class="left-section">
        <button
          class="hamburger-btn btn btn-ghost btn-icon"
          @click="emit('toggle-sidebar')"
          aria-label="Toggle Sidebar"
        >
          <span class="mdi mdi-menu"></span>
        </button>
        <router-link to="/" class="logo">
          <span class="logo-text">FairShare</span>
        </router-link>
      </div>

      <div class="right-section">
        <LanguageSelector />

        <button
          class="theme-toggle btn btn-ghost btn-icon"
          @click="toggleTheme"
          :aria-label="t('web.theme')"
        >
          <span v-if="theme === 'dark'" class="icon mdi mdi-weather-sunny"></span>
          <span v-else class="icon mdi mdi-weather-night"></span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import LanguageSelector from './LanguageSelector.vue';

const emit = defineEmits<{
  (e: 'toggle-sidebar'): void;
}>();

const { t } = useI18n();
const theme = ref<'light' | 'dark'>('light');

const applyTheme = (newTheme: 'light' | 'dark') => {
  theme.value = newTheme;
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('fairshare-theme', newTheme);
};

const toggleTheme = () => {
  const nextTheme = theme.value === 'light' ? 'dark' : 'light';
  applyTheme(nextTheme);
};

onMounted(() => {
  const savedTheme = localStorage.getItem('fairshare-theme') as 'light' | 'dark' | null;
  if (savedTheme === 'light' || savedTheme === 'dark') {
    applyTheme(savedTheme);
  } else {
    // Media query fallback
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(systemPrefersDark ? 'dark' : 'light');
  }
});
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-sticky);
  border-bottom: 1px solid var(--color-border);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: var(--max-width-lg);
  margin: 0 auto;
  padding: var(--space-3) var(--space-4);
  height: 64px;
}

.left-section {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.logo {
  text-decoration: none;
}

.logo-text {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.right-section {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.hamburger-btn {
  display: none;
  font-size: 1.3em;
}

.theme-toggle {
  font-size: 1.2em;
  padding: var(--space-2);
}

@media (max-width: 768px) {
  .hamburger-btn {
    display: inline-flex;
  }
}
</style>
