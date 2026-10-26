import { useEffect, useState } from 'react'
import { studyApi } from '../api/client.js'
import EmptyState from './EmptyState.jsx'

const blankForm = { title: '', content: '', is_public: false }
const formatDate = (value) => new Date(value).toLocaleString('ko-KR')

export default function StudyPage({ token }) {
  const [items, setItems] = useState([])
  const [form, setForm] = useState(blankForm)
  const [editingId, setEditingId] = useState(null)
  const [query, setQuery] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = async (search = query) => {
    setLoading(true)
    setError('')
    try { setItems(await studyApi.list(token, search)) }
    catch (requestError) { setError(requestError.message) }
    finally { setLoading(false) }
  }

  useEffect(() => {
    let active = true
    studyApi.list(token, '')
      .then((records) => { if (active) setItems(records) })
      .catch((requestError) => { if (active) setError(requestError.message) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [token])

  const submit = async (event) => {
    event.preventDefault()
    setError('')
    try {
      if (editingId) await studyApi.update(token, editingId, form)
      else await studyApi.create(token, form)
      setForm(blankForm)
      setEditingId(null)
      await load()
    } catch (requestError) { setError(requestError.message) }
  }

  const edit = (item) => {
    setEditingId(item.id)
    setForm({ title: item.title, content: item.content, is_public: item.is_public })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const remove = async (item) => {
    if (!window.confirm(`“${item.title}” 공부 기록을 삭제할까요? 삭제 후 되돌릴 수 없습니다.`)) return
    try { await studyApi.remove(token, item.id); await load() }
    catch (requestError) { setError(requestError.message) }
  }

  return (
    <section className="page-section">
      <div className="page-heading"><div><p className="eyebrow">Phase 6</p><h1>공부 기록</h1><p>오늘 배운 내용을 나중에 다시 찾을 수 있게 남겨보세요.</p></div></div>
      <div className="content-grid">
        <form className="panel stack-form editor-panel" onSubmit={submit}>
          <h2>{editingId ? '공부 기록 수정' : '새 공부 기록'}</h2>
          <label>제목<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} maxLength="100" required /></label>
          <label>내용<textarea value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} maxLength="5000" rows="8" required /></label>
          <label className="check-label"><input type="checkbox" checked={form.is_public} onChange={(e) => setForm({ ...form, is_public: e.target.checked })} />공개 기록으로 저장</label>
          {error && <p className="message error-message">{error}</p>}
          <div className="button-row"><button className="primary-button">{editingId ? '수정 저장' : '기록 저장'}</button>{editingId && <button type="button" className="secondary-button" onClick={() => { setEditingId(null); setForm(blankForm) }}>수정 취소</button>}</div>
        </form>
        <div className="list-column">
          <form className="search-row" onSubmit={(e) => { e.preventDefault(); load(query) }}><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="제목이나 내용 검색" /><button className="secondary-button">검색</button></form>
          {loading ? <EmptyState>기록을 불러오는 중입니다.</EmptyState> : items.length === 0 ? <EmptyState>아직 공부 기록이 없습니다.</EmptyState> : items.map((item) => <article className="record-card" key={item.id}><div className="record-meta"><span className={`badge ${item.is_public ? 'public' : ''}`}>{item.is_public ? '공개' : '비공개'}</span><time>{formatDate(item.created_at)}</time></div><h3>{item.title}</h3><p className="record-content">{item.content}</p><p className="updated-at">수정: {formatDate(item.updated_at)}</p><div className="button-row"><button className="secondary-button" onClick={() => edit(item)}>수정</button><button className="danger-button" onClick={() => remove(item)}>삭제</button></div></article>)}
        </div>
      </div>
    </section>
  )
}
