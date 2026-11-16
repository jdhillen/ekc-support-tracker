<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { api } from './api'
import { STATUSES } from './constants'
import StatsBar from './components/StatsBar.vue'
import RequestTable from './components/RequestTable.vue'
import RequestForm from './components/RequestForm.vue'

const requests = ref([])
const partners = ref([])
const stats = ref({})
const filters = reactive({ status: '', q: '' })
const loading = ref(true)
const error = ref('')

// null = dialog closed, {} = creating, {...request} = editing
const editing = ref(null)

async function loadRequests() {
  error.value = ''
  try {
    const [list, counts] = await Promise.all([api.listRequests(filters), api.stats()])
    requests.value = list
    stats.value = counts
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    partners.value = await api.listPartners()
  } catch (e) {
    error.value = e.message
  }
  await loadRequests()
})

// Re-query when filters change; debounce typing in the search box.
let searchTimer
watch(() => filters.status, loadRequests)
watch(() => filters.q, () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(loadRequests, 300)
})

async function save(payload) {
  if (editing.value?.id) {
    await api.updateRequest(editing.value.id, payload)
  } else {
    await api.createRequest(payload)
  }
  editing.value = null
  await loadRequests()
}

async function remove() {
  await api.deleteRequest(editing.value.id)
  editing.value = null
  await loadRequests()
}

async function quickStatus(request, status) {
  try {
    await api.updateRequest(request.id, { status })
    await loadRequests()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <header class="app-header">
    <div>
      <h1>Founder Support Tracker</h1>
      <p class="subtitle">Log entrepreneur requests and route them to the right regional partner.</p>
    </div>
    <button class="btn primary" @click="editing = {}">+ New request</button>
  </header>

  <main>
    <StatsBar :stats="stats" :active="filters.status" @select="filters.status = $event" />

    <div class="toolbar">
      <input
        v-model="filters.q"
        type="search"
        placeholder="Search title, founder, or business…"
        aria-label="Search requests"
      />
      <select v-model="filters.status" aria-label="Filter by status">
        <option value="">All statuses</option>
        <option v-for="s in STATUSES" :key="s.value" :value="s.value">{{ s.label }}</option>
      </select>
    </div>

    <p v-if="error" class="alert" role="alert">{{ error }}</p>
    <p v-if="loading" class="muted">Loading…</p>
    <RequestTable
      v-else
      :requests="requests"
      @open="editing = { ...$event }"
      @status="quickStatus"
    />
  </main>

  <RequestForm
    v-if="editing"
    :request="editing"
    :partners="partners"
    :on-save="save"
    :on-delete="remove"
    @close="editing = null"
  />
</template>
