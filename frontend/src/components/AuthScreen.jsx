import { useState } from 'react'
import { authApi } from '../api/client.js'

export default function AuthScreen({ onAuthenticated }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ email: '', password: '', nickname: '' })
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value })

  const submit = async (event) => {
    event.preventDefault()
    setError('')
    setSubmitting(true)
    try {
      const result = mode === 'register'
        ? await authApi.register(form)
        : await authApi.login({ email: form.email, password: form.password })
      onAuthenticated(result)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-intro">
        <p className="eyebrow">BuildLog</p>
        <h1>배운 내용과 해결 과정을 한곳에 기록하세요.</h1>
        <p>공부 기록, 할 일, 오류 해결 과정을 잊지 않고 다시 찾을 수 있습니다.</p>
      </section>
      <section className="panel auth-panel">
        <div className="segmented" aria-label="회원 화면 선택">
          <button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>로그인</button>
          <button className={mode === 'register' ? 'active' : ''} onClick={() => setMode('register')}>회원가입</button>
        </div>
        <h2>{mode === 'login' ? '다시 만나서 반가워요' : 'BuildLog 시작하기'}</h2>
        <form onSubmit={submit} className="stack-form">
          <label>이메일<input name="email" type="email" value={form.email} onChange={update} required autoComplete="email" /></label>
          <label>비밀번호<input name="password" type="password" value={form.password} onChange={update} required minLength={mode === 'register' ? 8 : 1} autoComplete={mode === 'register' ? 'new-password' : 'current-password'} /></label>
          {mode === 'register' && <label>닉네임<input name="nickname" value={form.nickname} onChange={update} required minLength="2" maxLength="20" placeholder="한글, 영문, 숫자, 밑줄" /></label>}
          {error && <p className="message error-message">{error}</p>}
          <button className="primary-button" disabled={submitting}>{submitting ? '처리 중...' : mode === 'login' ? '로그인' : '가입하고 시작하기'}</button>
        </form>
      </section>
    </main>
  )
}
