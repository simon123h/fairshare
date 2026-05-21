<template>
  <div class="participant-manager card">
    <h2 class="section-title">
      <span class="mdi mdi-account-group"></span> {{ t('web.participants') }}
    </h2>

    <div class="manager-content">
      <div class="input-area">
        <span class="mdi mdi-account-plus-outline input-icon"></span>
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

      <div class="participants-display">
        <TransitionGroup name="list" tag="div" class="chips-grid">
          <div
            v-for="person in participants"
            :key="person"
            class="chip chip-interactive participant-chip"
          >
            <span class="mdi mdi-account-outline"></span>
            <span class="person-name">{{ person }}</span>
            <button
              type="button"
              class="chip-remove"
              @click="remove(person)"
              aria-label="Remove participant"
            >
              <span class="mdi mdi-close"></span>
            </button>
          </div>
        </TransitionGroup>

        <p v-if="participants.length === 0" class="empty-text">
          {{ t('web.getStarted') }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps<{
  participants: string[];
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
  gap: var(--space-4);
  padding: var(--space-6);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  margin: 0;
}

.manager-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.input-area {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-3);
  background: var(--color-bg-alt);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  transition: all var(--transition-fast);
  max-width: 320px;
}

.input-area:focus-within {
  border-color: var(--color-primary);
  background: var(--color-surface);
  box-shadow: 0 0 0 3px var(--color-primary-50);
}

.input-icon {
  font-size: 1.125rem;
  color: var(--color-text-muted);
}

.inline-input {
  flex: 1;
  border: none;
  background: transparent;
  color: var(--color-text);
  font-size: var(--font-size-sm);
}

.inline-input:focus {
  outline: none;
}

.chips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--space-3);
}

.participant-chip {
  justify-content: space-between;
  padding: var(--space-2) var(--space-3);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.person-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin: 0 var(--space-2);
}

.empty-text {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin: 0;
  padding: var(--space-8);
  text-align: center;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
}

/* Animations */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
