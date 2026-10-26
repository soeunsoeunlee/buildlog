const apiBaseUrl = (
  import.meta.env.VITE_API_BASE_URL ?? '/api'
).replace(/\/$/, '')

async function apiRequest(path, options = {}) {
  let response

  try {
    response = await fetch(`${apiBaseUrl}${path}`, {
      ...options,
      headers: {
        Accept: 'application/json',
        ...options.headers,
      },
    })
  } catch {
    throw new Error('서버에 연결할 수 없습니다.')
  }

  if (!response.ok) {
    throw new Error(`요청을 처리하지 못했습니다. (${response.status})`)
  }

  return response.json()
}

export function getHealth() {
  return apiRequest('/health')
}
