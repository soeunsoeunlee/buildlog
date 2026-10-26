import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App.jsx'

beforeEach(() => localStorage.clear())

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('회원 화면', () => {
  it('로그인과 회원가입 입력 화면을 전환한다', () => {
    render(<App />)

    expect(screen.getAllByRole('button', { name: '로그인' })).toHaveLength(2)
    fireEvent.click(screen.getByRole('button', { name: '회원가입' }))
    expect(screen.getByLabelText('닉네임')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: '가입하고 시작하기' })).toBeInTheDocument()
  })

  it('로그인에 성공하면 내 기록 홈을 보여준다', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        token: 'test-token',
        user: { id: 1, email: 'user@example.com', nickname: '테스트사용자', is_admin: false },
      }),
    }))
    render(<App />)

    fireEvent.change(screen.getByLabelText('이메일'), { target: { value: 'user@example.com' } })
    fireEvent.change(screen.getByLabelText('비밀번호'), { target: { value: 'password123' } })
    fireEvent.submit(screen.getByLabelText('비밀번호').closest('form'))

    expect(await screen.findByText('테스트사용자님의 BuildLog')).toBeInTheDocument()
    expect(localStorage.getItem('buildlog_token')).toBe('test-token')
  })

  it('로그인 실패 시 입력값과 안내를 유지한다', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
      json: async () => ({ error: { message: '이메일 또는 비밀번호가 맞지 않습니다.' } }),
    }))
    render(<App />)

    const email = screen.getByLabelText('이메일')
    fireEvent.change(email, { target: { value: 'user@example.com' } })
    fireEvent.change(screen.getByLabelText('비밀번호'), { target: { value: 'wrong' } })
    fireEvent.submit(screen.getByLabelText('비밀번호').closest('form'))

    expect(await screen.findByText('이메일 또는 비밀번호가 맞지 않습니다.')).toBeInTheDocument()
    expect(email).toHaveValue('user@example.com')
  })
})
