// Thin client for the FastAPI service. All calls are same-origin under /api.

async function call(path, { method = 'GET', body } = {}) {
  const res = await fetch(`/api${path}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (res.status === 204) return null
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(errorMessage(data) || `Request failed (${res.status})`)
  return data
}

// FastAPI returns either { detail: "msg" } or { detail: [{ loc, msg }, ...] } for validation errors.
function errorMessage(data) {
  if (typeof data.detail === 'string') return data.detail
  if (Array.isArray(data.detail)) {
    return data.detail.map((d) => `${d.loc?.at(-1) ?? 'field'}: ${d.msg}`).join('; ')
  }
  return null
}

export const api = {
  listPartners: () => call('/partners'),
  stats: () => call('/stats'),
  listRequests: ({ status, q } = {}) => {
    const params = new URLSearchParams()
    if (status) params.set('status', status)
    if (q) params.set('q', q)
    const qs = params.toString()
    return call(`/requests${qs ? `?${qs}` : ''}`)
  },
  createRequest: (data) => call('/requests', { method: 'POST', body: data }),
  updateRequest: (id, data) => call(`/requests/${id}`, { method: 'PATCH', body: data }),
  deleteRequest: (id) => call(`/requests/${id}`, { method: 'DELETE' }),
}
