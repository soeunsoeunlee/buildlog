import { useEffect, useState } from 'react'
import { authApi } from './api/client.js'
import AccountPage from './components/AccountPage.jsx'
import AuthScreen from './components/AuthScreen.jsx'
import ErrorPage from './components/ErrorPage.jsx'
import StudyPage from './components/StudyPage.jsx'
import TodoPage from './components/TodoPage.jsx'
import './App.css'

const TOKEN_KEY = 'buildlog_token'
const pages = [
  ['home', '홈'],
  ['studies', '공부 기록'],
  ['todos', '할 일'],
  ['errors', '오류 기록'],
  ['account', '계정 설정'],
]

function Home({ user, navigate }) {
  return (
    <section className="page-section home-page">
      <div className="home-hero">
        <p className="eyebrow">{user.nickname}님의 BuildLog</p>
        <h1>오늘의 배움과 막혔던 순간을 기록해 보세요.</h1>
        <p>기록은 기본적으로 나만 볼 수 있습니다. 공개 여부는 각 기록에서 선택할 수 있어요.</p>
      </div>
      <div className="feature-grid">
        <button className="feature-card" onClick={() => navigate('studies')}><span>01</span><h2>공부 기록</h2><p>오늘 배운 내용과 작업 과정을 남깁니다.</p></button>
        <button className="feature-card" onClick={() => navigate('todos')}><span>02</span><h2>할 일</h2><p>앞으로 할 일과 완료한 일을 구분합니다.</p></button>
        <button className="feature-card" onClick={() => navigate('errors')}><span>03</span><h2>오류 기록</h2><p>오류 원인과 해결 방법을 모아둡니다.</p></button>
      </div>
    </section>
  )
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY))
  const [user, setUser] = useState(null)
  const [page, setPage] = useState('home')
  const [loading, setLoading] = useState(Boolean(token))

  useEffect(() => {
    if (!token) return
    authApi.me(token)
      .then(setUser)
      .catch(() => { localStorage.removeItem(TOKEN_KEY); setToken(null) })
      .finally(() => setLoading(false))
  }, [token])

  const authenticated = ({ token: nextToken, user: nextUser }) => {
    localStorage.setItem(TOKEN_KEY, nextToken)
    setToken(nextToken)
    setUser(nextUser)
    setPage('home')
  }

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
    setUser(null)
    setPage('home')
  }

  if (loading) return <main className="loading-page">로그인 상태를 확인하고 있습니다.</main>
  if (!token || !user) return <AuthScreen onAuthenticated={authenticated} />

  return (
    <div className="app-shell">
      <header className="site-header">
        <button className="brand" onClick={() => setPage('home')}>BuildLog</button>
        <nav aria-label="주 메뉴">{pages.map(([value, label]) => <button key={value} className={page === value ? 'active' : ''} onClick={() => setPage(value)}>{label}</button>)}</nav>
        <div className="user-menu"><span>{user.nickname}</span><button className="text-button" onClick={logout}>로그아웃</button></div>
      </header>
      <main>
        {page === 'home' && <Home user={user} navigate={setPage} />}
        {page === 'studies' && <StudyPage token={token} />}
        {page === 'todos' && <TodoPage token={token} />}
        {page === 'errors' && <ErrorPage token={token} />}
        {page === 'account' && <AccountPage token={token} user={user} onUserChange={setUser} />}
      </main>
    </div>
  )
}

export default App
