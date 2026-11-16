<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { CATEGORIES, PRIORITIES, STATUSES } from '../constants'

// onSave / onDelete are async functions from the parent, so the form can await them and show errors.
const props = defineProps({ request: Object, partners: Array, onSave: Function, onDelete: Function })
const emit = defineEmits(['close'])

const isEdit = computed(() => Boolean(props.request.id))
const dialog = ref(null)
const saving = ref(false)
const error = ref('')

const form = reactive({
  title: props.request.title ?? '',
  description: props.request.description ?? '',
  requester_name: props.request.requester_name ?? '',
  requester_email: props.request.requester_email ?? '',
  business_name: props.request.business_name ?? '',
  category: props.request.category ?? 'capital',
  priority: props.request.priority ?? 'medium',
  status: props.request.status ?? 'new',
  partner_id: props.request.partner_id ?? '',
})

onMounted(() => dialog.value.showModal())

async function run(action) {
  saving.value = true
  error.value = ''
  try {
    await action()
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

function submit() {
  const payload = { ...form, partner_id: form.partner_id === '' ? null : Number(form.partner_id) }
  if (!isEdit.value) delete payload.status // new requests always start as "new"
  run(() => props.onSave(payload))
}

function confirmDelete() {
  if (window.confirm('Delete this request? This cannot be undone.')) {
    run(() => props.onDelete())
  }
}
</script>

<template>
  <dialog ref="dialog" class="dialog" @close="emit('close')">
    <form @submit.prevent="submit">
      <h2>{{ isEdit ? 'Edit request' : 'New support request' }}</h2>

      <label>Title *
        <input v-model.trim="form.title" required minlength="3" maxlength="200" />
      </label>
      <label>Description
        <textarea v-model="form.description" rows="3" maxlength="4000" />
      </label>

      <div class="row">
        <label>Founder name *
          <input v-model.trim="form.requester_name" required maxlength="120" />
        </label>
        <label>Founder email *
          <input v-model.trim="form.requester_email" type="email" required maxlength="254" />
        </label>
      </div>
      <label>Business name
        <input v-model.trim="form.business_name" maxlength="200" />
      </label>

      <div class="row">
        <label>Category *
          <select v-model="form.category">
            <option v-for="c in CATEGORIES" :key="c.value" :value="c.value">{{ c.label }}</option>
          </select>
        </label>
        <label>Priority
          <select v-model="form.priority">
            <option v-for="p in PRIORITIES" :key="p.value" :value="p.value">{{ p.label }}</option>
          </select>
        </label>
      </div>

      <div class="row">
        <label>Partner organization
          <select v-model="form.partner_id">
            <option value="">Unassigned</option>
            <option v-for="p in partners" :key="p.id" :value="p.id" :title="p.focus">{{ p.name }}</option>
          </select>
        </label>
        <label v-if="isEdit">Status
          <select v-model="form.status">
            <option v-for="s in STATUSES" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
        </label>
      </div>

      <p v-if="error" class="alert" role="alert">{{ error }}</p>

      <div class="actions">
        <button v-if="isEdit" type="button" class="btn danger" :disabled="saving" @click="confirmDelete">Delete</button>
        <span class="spacer" />
        <button type="button" class="btn" :disabled="saving" @click="dialog.close()">Cancel</button>
        <button type="submit" class="btn primary" :disabled="saving">{{ saving ? 'Saving…' : 'Save' }}</button>
      </div>
    </form>
  </dialog>
</template>
