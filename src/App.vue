<template>
  <div class="app-container">
    <AppHeader @toggle-sidebar="toggleSidebar" />
    
    <div class="main-layout">
      <ProjectSidebar :isOpen="isSidebarOpen" @close="closeSidebar" />
      
      <div class="content-area">
        <router-view v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { useI18n } from 'vue-i18n';
import AppHeader from './components/AppHeader.vue';
import ProjectSidebar from './components/ProjectSidebar.vue';

const { locale } = useI18n();
const isSidebarOpen = ref(false);

// Synchronize the HTML lang attribute with the current locale for CSS :lang() selectors and accessibility
watchEffect(() => {
  document.documentElement.setAttribute('lang', locale.value);
});

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const closeSidebar = () => {
  isSidebarOpen.value = false;
};
</script>

<style>
/* Root Global Layout Styles */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-family);
  transition: background-color var(--transition-normal), color var(--transition-normal);
}

.main-layout {
  display: flex;
  flex: 1;
  position: relative;
}

.content-area {
  flex: 1;
  min-width: 0;
  padding: var(--space-4);
  overflow-y: auto;
}

@media (max-width: 768px) {
  .content-area {
    padding: var(--space-2);
  }
}
</style>
