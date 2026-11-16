<script setup>
import { STATUSES } from '../constants'
import { CheckCircle2, Clock, Forward, Inbox } from 'lucide-vue-next'

defineProps({ stats: Object, active: String })
const emit = defineEmits(['select'])

const icons = { new: Inbox, referred: Forward, in_progress: Clock, resolved: CheckCircle2 }
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
      <span class="stat-icon"><component :is="icons[s.value]" :size="22" aria-hidden="true" /></span>
      <span class="stat-text">
        <span class="stat-count">{{ stats[s.value] ?? 0 }}</span>
        <span class="stat-label">{{ s.label }}</span>
      </span>
    </button>
  </div>
</template>
