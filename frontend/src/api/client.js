const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL ?? '/api').replace(/\/$/, '')

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiRequest(path, { token, body, headers, ...options } = {}) {
  let response
  try {
    response = await fetch(`${apiBaseUrl}${path}`, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...headers,
      },
      ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
    })
  } catch {
    throw new ApiError('서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인해 주세요.', 0)
  }

  if (response.status === 204) return null
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new ApiError(data?.error?.message ?? '요청을 처리하지 못했습니다.', response.status)
  }
  return data
}

export const authApi = {
  register: (body) => apiRequest('/auth/register', { method: 'POST', body }),
  login: (body) => apiRequest('/auth/login', { method: 'POST', body }),
  me: (token) => apiRequest('/auth/me', { token }),
  updateNickname: (token, nickname) =>
    apiRequest('/auth/me/nickname', { method: 'PATCH', token, body: { nickname } }),
}

export const studyApi = {
  list: (token, query = '') => apiRequest(`/studies?q=${encodeURIComponent(query)}`, { token }),
  create: (token, body) => apiRequest('/studies', { method: 'POST', token, body }),
  update: (token, id, body) => apiRequest(`/studies/${id}`, { method: 'PUT', token, body }),
  remove: (token, id) => apiRequest(`/studies/${id}`, { method: 'DELETE', token }),
}

export const todoApi = {
  list: (token, state = 'all') => apiRequest(`/todos?state=${state}`, { token }),
  create: (token, body) => apiRequest('/todos', { method: 'POST', token, body }),
  update: (token, id, body) => apiRequest(`/todos/${id}`, { method: 'PUT', token, body }),
  setCompleted: (token, id, isCompleted) =>
    apiRequest(`/todos/${id}/status`, {
      method: 'PATCH',
      token,
      body: { is_completed: isCompleted },
    }),
  remove: (token, id) => apiRequest(`/todos/${id}`, { method: 'DELETE', token }),
}

export const errorApi = {
  list: (token, state = 'all', query = '') =>
    apiRequest(`/errors?state=${state}&q=${encodeURIComponent(query)}`, { token }),
  create: (token, body) => apiRequest('/errors', { method: 'POST', token, body }),
  update: (token, id, body) => apiRequest(`/errors/${id}`, { method: 'PUT', token, body }),
  remove: (token, id) => apiRequest(`/errors/${id}`, { method: 'DELETE', token }),
}
