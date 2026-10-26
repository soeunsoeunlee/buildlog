import { useState } from 'react'
import { authApi } from '../api/client.js'

export default function AccountPage({ token, user, onUserChange }) {
  const [nickname, setNickname] = useState(user.nickname)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const submit = async (event) => {
    event.preventDefault()
    setMessage('')
    setError('')
    try {
      const updated = await authApi.updateNickname(token, nickname)
      onUserChange(updated)
      setNickname(updated.nickname)
      setMessage('닉네임을 변경했습니다.')
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  return (
    <section className="page-section narrow-section">
      <div className="page-heading"><div><p className="eyebrow">계정 설정</p><h1>내 정보</h1></div></div>
      <div className="panel">
        <p className="account-email">가입 이메일: {user.email}</p>
        <form className="stack-form" onSubmit={submit}>
          <label>닉네임<input value={nickname} onChange={(e) => setNickname(e.target.value)} minLength="2" maxLength="20" required /></label>
          {message && <p className="message success-message">{message}</p>}
          {error && <p className="message error-message">{error}</p>}
          <button className="primary-button">닉네임 변경</button>
        </form>
      </div>
    </section>
  )
}
