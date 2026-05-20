<template>
  <div class="participant-manager card">
    <h2 class="section-title">
      <span>👥</span> {{ t('web.participants') }}
    </h2>

    <div class="input-area">
      <div class="chips-container">
        <TransitionGroup name="list">
          <div
            v-for="person in participants"
            :key="person"
            class="chip chip-interactive hover-lift"
          >
            <span>{{ person }}</span>
            <button
              type="button"
              class="chip-remove"
              @click="remove(person)"
              aria-label="Remove participant"
            >
              ✕
            </button>
          </div>
        </TransitionGroup>

        <!-- Input for adding participants inline -->
        <input
          type="text"
          v-model="newPerson"
          :placeholder="t('web.addParticipant')"
          class="inline-input"
          @keydown.enter.prevent="addFromInput"
          @keydown.comma.prevent="addFromInput"
          @blur="addFromInput"
          @paste="handlePaste"
        />
      </div>
    </div>

    <p v-if="participants.length === 0" class="empty-text">
      {{ t('web.getStarted') }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps<{
  participants: string[];
  currency: string;
}>();

const emit = defineEmits<{
  (e: 'update:participants', value: string[]): void;
}>();

const { t } = useI18n();
const newPerson = ref('');

const addNames = (names: string[]) => {
  const currentList = [...props.participants];
  let changed = false;

  names.forEach(name => {
    const trimmed = name.trim();
    if (trimmed && !currentList.includes(trimmed)) {
      currentList.push(trimmed);
      changed = true;
    }
  });

  if (changed) {
    emit('update:participants', currentList);
  }
};

const addFromInput = () => {
  const val = newPerson.value;
  if (!val.trim()) return;

  // Split by comma in case they typed with comma
  const parts = val.split(',');
  addNames(parts);
  newPerson.value = '';
};

const handlePaste = (e: ClipboardEvent) => {
  e.preventDefault();
  const text = e.clipboardData?.getData('text') || '';
  // Split by commas or newlines
  const parts = text.split(/[,\n]/);
  addNames(parts);
  newPerson.value = '';
};

const remove = (name: string) => {
  const currentList = props.participants.filter(p => p !== name);
  emit('update:participants', currentList);
};
</script>

<style scoped>
.participant-manager {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  padding: var(--space-4);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0;
}

.input-area {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-2);
  background: var(--color-bg-alt);
  min-height: 48px;
  display: flex;
  align-items: center;
  transition: border-color var(--transition-fast);
}

.input-area:focus-within {
  border-color: var(--color-primary);
  background: var(--color-surface);
}

.chips-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  width: 100%;
}

.inline-input {
  flex: 1;
  min-width: 120px;
  border: none;
  background: transparent;
  color: var(--color-text);
  font-size: var(--font-size-sm);
  padding: var(--space-1) var(--space-2);
}

.inline-input:focus {
  outline: none;
}

.empty-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
  text-align: center;
}
</style>
