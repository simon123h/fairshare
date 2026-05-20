<template>
  <div class="currency-selector">
    <div class="pills">
      <button
        v-for="preset in presets"
        :key="preset.symbol"
        type="button"
        class="pill"
        :class="{ active: isPresetSelected(preset.symbol) }"
        @click="selectPreset(preset.symbol)"
      >
        <span class="symbol">{{ preset.symbol }}</span>
        <span class="label">{{ preset.label }}</span>
      </button>

      <button
        type="button"
        class="pill"
        :class="{ active: isCustomSelected }"
        @click="selectCustom"
      >
        {{ t('web.customCurrency') }}
      </button>
    </div>

    <Transition name="slide">
      <div v-if="isCustomSelected" class="custom-input-container">
        <input
          ref="customInputRef"
          type="text"
          class="custom-input"
          :placeholder="t('web.currency')"
          v-model="customValue"
          @input="onCustomInput"
          maxlength="8"
        />
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const { t } = useI18n();

const presets = [
  { symbol: '€', label: 'EUR' },
  { symbol: '$', label: 'USD' },
  { symbol: '£', label: 'GBP' },
  { symbol: '¥', label: 'JPY' },
  { symbol: 'Fr', label: 'CHF' },
  { symbol: 'kr', label: 'SEK' }
];

const customValue = ref('');
const isCustomSelected = ref(false);
const customInputRef = ref<HTMLInputElement | null>(null);

// Initialize selections based on modelValue
const initSelection = () => {
  const isPreset = presets.some(p => p.symbol === props.modelValue);
  if (isPreset) {
    isCustomSelected.value = false;
    customValue.value = '';
  } else {
    isCustomSelected.value = true;
    customValue.value = props.modelValue;
  }
};

initSelection();

watch(() => props.modelValue, () => {
  initSelection();
});

const isPresetSelected = (symbol: string) => {
  return !isCustomSelected.value && props.modelValue === symbol;
};

const selectPreset = (symbol: string) => {
  isCustomSelected.value = false;
  emit('update:modelValue', symbol);
};

const selectCustom = async () => {
  isCustomSelected.value = true;
  // Fallback if customValue is empty
  if (!customValue.value) {
    customValue.value = '¤';
    emit('update:modelValue', '¤');
  } else {
    emit('update:modelValue', customValue.value);
  }
  await nextTick();
  customInputRef.value?.focus();
};

const onCustomInput = () => {
  emit('update:modelValue', customValue.value.trim());
};
</script>

<style scoped>
.currency-selector {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.pills {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.pill {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.pill:hover {
  background: var(--color-border-light);
  color: var(--color-text);
  border-color: var(--color-text-muted);
}

.pill.active {
  background: var(--color-primary);
  color: var(--color-text-on-primary);
  border-color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.symbol {
  font-weight: var(--font-weight-bold);
}

.label {
  font-size: 0.85em;
  opacity: 0.8;
}

.custom-input-container {
  overflow: hidden;
}

.custom-input {
  width: 100%;
  max-width: 120px;
  padding: var(--space-2) var(--space-3);
  font-size: var(--font-size-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  transition: border-color var(--transition-fast);
}

.custom-input:focus {
  outline: none;
  border-color: var(--color-primary);
}
</style>
