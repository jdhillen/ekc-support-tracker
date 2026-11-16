<script setup>
import { CATEGORIES, PRIORITIES, STATUSES, labelFor } from '../constants'

defineProps({ requests: Array })
const emit = defineEmits(['open', 'status'])

const formatDate = (iso) =>
  new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
</script>

<template>
  <p v-if="!requests.length" class="empty">No requests match these filters.</p>
  <div v-else class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>Request</th>
          <th>Founder</th>
          <th>Category</th>
          <th>Priority</th>
          <th>Partner</th>
          <th>Status</th>
          <th>Updated</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in requests" :key="r.id">
          <td>
            <button class="link" @click="emit('open', r)">{{ r.title }}</button>
            <div class="muted small">{{ r.business_name }}</div>
          </td>
          <td>{{ r.requester_name }}</td>
          <td>{{ labelFor(CATEGORIES, r.category) }}</td>
          <td><span class="pill" :class="`priority-${r.priority}`">{{ labelFor(PRIORITIES, r.priority) }}</span></td>
          <td>
            <span v-if="r.partner_name">{{ r.partner_name }}</span>
            <span v-else class="muted">Unassigned</span>
          </td>
          <td>
            <select
              class="status-select"
              :class="`status-${r.status}`"
              :value="r.status"
              :aria-label="`Status for ${r.title}`"
              @change="emit('status', r, $event.target.value)"
            >
              <option v-for="s in STATUSES" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </td>
          <td class="muted small">{{ formatDate(r.updated_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
