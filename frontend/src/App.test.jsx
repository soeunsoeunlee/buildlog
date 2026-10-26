import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import App from './App.jsx'

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('서버 연결 상태 화면', () => {
  it('FastAPI 상태 응답을 받으면 정상 연결을 안내한다', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ status: 'ok', service: 'BuildLog API' }),
      }),
    )

    render(<App />)

    expect(
      await screen.findByText('BuildLog API 백엔드에 정상적으로 연결되었습니다.'),
    ).toBeInTheDocument()
    expect(fetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/api\/health$/),
      expect.objectContaining({
        headers: expect.objectContaining({ Accept: 'application/json' }),
      }),
    )
  })

  it('FastAPI에 연결하지 못하면 확인 방법을 안내한다', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('network error')))

    render(<App />)

    expect(
      await screen.findByText(
        '백엔드에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인해 주세요.',
      ),
    ).toBeInTheDocument()
  })
})
