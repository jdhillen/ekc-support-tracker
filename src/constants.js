// Mirrors the Literal types in api/_schemas.py and the CHECK constraints in db/schema.sql.
export const STATUSES = [
  { value: 'new', label: 'New' },
  { value: 'referred', label: 'Referred' },
  { value: 'in_progress', label: 'In progress' },
  { value: 'resolved', label: 'Resolved' },
]

export const CATEGORIES = [
  { value: 'capital', label: 'Capital' },
  { value: 'legal', label: 'Legal' },
  { value: 'talent', label: 'Talent & hiring' },
  { value: 'mentorship', label: 'Mentorship' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'other', label: 'Other' },
]

export const PRIORITIES = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
]

export const labelFor = (list, value) => list.find((o) => o.value === value)?.label ?? value
