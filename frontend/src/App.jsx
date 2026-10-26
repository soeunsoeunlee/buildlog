import { useEffect, useState } from 'react'
import { getHealth } from './api/client.js'
import './App.css'

const initialHealth = {
  state: 'loading',
  message: '백엔드 연결을 확인하고 있습니다.',
}

function App() {
  const [health, setHealth] = useState(initialHealth)

  useEffect(() => {
    let active = true

    getHealth()
      .then((result) => {
        if (active) {
          setHealth({
            state: 'success',
            message: `${result.service} 백엔드에 정상적으로 연결되었습니다.`,
          })
        }
      })
      .catch(() => {
        if (active) {
          setHealth({
            state: 'error',
            message:
              '백엔드에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인해 주세요.',
          })
        }
      })

    return () => {
      active = false
    }
  }, [])

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="BuildLog 홈">
          BuildLog
        </a>
        <span className="phase-label">개발 준비 화면</span>
      </header>

      <main className="main-content">
        <section className="intro-card">
          <p className="eyebrow">나의 공부와 해결 과정을 한곳에</p>
          <h1>배운 내용이 사라지지 않도록 기록하세요.</h1>
          <p className="intro-text">
            BuildLog는 공부 기록, 할 일, 오류 해결 과정을 모아보는 서비스입니다.
            지금은 화면과 서버의 연결 상태를 확인하는 단계입니다.
          </p>
        </section>

        <section className="status-card" aria-live="polite">
          <div className={`status-dot status-dot--${health.state}`} aria-hidden="true" />
          <div>
            <h2>서버 연결 상태</h2>
            <p data-testid="health-message">{health.message}</p>
          </div>
        </section>

        <section className="form-preview" aria-labelledby="style-preview-title">
          <h2 id="style-preview-title">공통 화면 스타일</h2>
          <p>앞으로 사용할 카드, 입력칸과 버튼의 기본 모양을 준비했습니다.</p>
          <label htmlFor="preview-input">입력칸 예시</label>
          <input id="preview-input" placeholder="내용을 입력하세요" disabled />
          <button type="button" disabled>
            저장 버튼 예시
          </button>
        </section>
      </main>
    </div>
  )
}

export default App
