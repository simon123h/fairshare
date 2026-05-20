<template>
  <div class="language-selector" ref="dropdownRef">
    <button @click="toggleDropdown" class="btn btn-ghost select-btn" aria-haspopup="listbox" :aria-expanded="isOpen">
      <span class="flag">{{ currentLocaleInfo?.flag }}</span>
      <span class="lang-name">{{ currentLocaleInfo?.name }}</span>
      <span class="arrow" :class="{ open: isOpen }">▼</span>
    </button>

    <Transition name="fade">
      <ul v-if="isOpen" class="dropdown-menu" role="listbox">
        <li
          v-for="loc in SUPPORTED_LOCALES"
          :key="loc.code"
          @click="selectLocale(loc.code)"
          class="dropdown-item"
          :class="{ active: loc.code === locale }"
          role="option"
          :aria-selected="loc.code === locale"
        >
          <span class="flag">{{ loc.flag }}</span>
          <span class="name">{{ loc.name }}</span>
        </li>
      </ul>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { SUPPORTED_LOCALES } from '../composables/useI18n';

const { locale } = useI18n();
const isOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);

const currentLocaleInfo = computed(() => {
  return SUPPORTED_LOCALES.find(loc => loc.code === locale.value) || SUPPORTED_LOCALES[0];
});

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const selectLocale = (code: string) => {
  locale.value = code;
  localStorage.setItem('fairshare-locale', code);
  isOpen.value = false;
};

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.language-selector {
  position: relative;
  display: inline-block;
}

.select-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  color: var(--color-text);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.select-btn:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-text-secondary);
}

.flag {
  font-size: 1.1em;
}

.arrow {
  font-size: 0.7em;
  transition: transform var(--transition-fast);
  color: var(--color-text-secondary);
}

.arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 105%;
  right: 0;
  z-index: var(--z-dropdown);
  min-width: 140px;
  margin: 0;
  padding: var(--space-1) 0;
  list-style: none;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  transform-origin: top right;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-text);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.dropdown-item:hover {
  background: var(--color-surface-hover);
}

.dropdown-item.active {
  background: var(--color-primary-50);
  color: var(--color-primary);
  font-weight: var(--font-weight-semibold);
}

@media (max-width: 768px) {
  .lang-name {
    display: none;
  }
}
</style>
