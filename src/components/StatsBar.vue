<script setup>
import { STATUSES } from '../constants'

defineProps({ stats: Object, active: String })
const emit = defineEmits(['select'])
</script>

<template>
  <div class="stats">
    <button
      v-for="s in STATUSES"
      :key="s.value"
      class="stat"
      :class="[`status-${s.value}`, { active: active === s.value }]"
      :aria-pressed="active === s.value"
      @click="emit('select', active === s.value ? '' : s.value)"
    >
      <span class="stat-count">{{ stats[s.value] ?? 0 }}</span>
      <span class="stat-label">{{ s.label }}</span>
    </button>
  </div>
</template>
