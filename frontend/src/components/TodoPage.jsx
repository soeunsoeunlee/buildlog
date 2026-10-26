import { useEffect, useState } from 'react'
import { todoApi } from '../api/client.js'
import EmptyState from './EmptyState.jsx'

const blankForm = { title: '', is_public: false }
const filters = [['all', '전체'], ['pending', '남은 일'], ['completed', '완료한 일']]
const formatDate = (value) => new Date(value).toLocaleString('ko-KR')

export default function TodoPage({ token }) {
  const [items, setItems] = useState([])
  const [form, setForm] = useState(blankForm)
  const [editingId, setEditingId] = useState(null)
  const [filter, setFilter] = useState('all')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = async (nextFilter = filter) => {
    setLoading(true); setError('')
    try { setItems(await todoApi.list(token, nextFilter)) }
    catch (requestError) { setError(requestError.message) }
    finally { setLoading(false) }
  }
  useEffect(() => {
    let active = true
    todoApi.list(token, filter)
      .then((records) => { if (active) setItems(records) })
      .catch((requestError) => { if (active) setError(requestError.message) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [token, filter])

  const submit = async (event) => {
    event.preventDefault(); setError('')
    try {
      if (editingId) await todoApi.update(token, editingId, form)
      else await todoApi.create(token, form)
      setForm(blankForm); setEditingId(null); await load()
    } catch (requestError) { setError(requestError.message) }
  }
  const toggle = async (item) => { try { await todoApi.setCompleted(token, item.id, !item.is_completed); await load() } catch (e) { setError(e.message) } }
  const remove = async (item) => { if (!window.confirm(`“${item.title}” 할 일을 삭제할까요?`)) return; try { await todoApi.remove(token, item.id); await load() } catch (e) { setError(e.message) } }

  return (
    <section className="page-section">
      <div className="page-heading"><div><p className="eyebrow">Phase 7</p><h1>할 일</h1><p>남은 일과 끝낸 일을 한눈에 확인하세요.</p></div></div>
      <div className="content-grid">
        <form className="panel stack-form editor-panel" onSubmit={submit}><h2>{editingId ? '할 일 수정' : '새 할 일'}</h2><label>제목<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} maxLength="100" required /></label><label className="check-label"><input type="checkbox" checked={form.is_public} onChange={(e) => setForm({ ...form, is_public: e.target.checked })} />공개 할 일로 저장</label>{error && <p className="message error-message">{error}</p>}<div className="button-row"><button className="primary-button">{editingId ? '수정 저장' : '할 일 저장'}</button>{editingId && <button type="button" className="secondary-button" onClick={() => { setEditingId(null); setForm(blankForm) }}>수정 취소</button>}</div></form>
        <div className="list-column"><div className="segmented filter-row">{filters.map(([value, label]) => <button key={value} className={filter === value ? 'active' : ''} onClick={() => { setLoading(true); setFilter(value) }}>{label}</button>)}</div>{loading ? <EmptyState>할 일을 불러오는 중입니다.</EmptyState> : items.length === 0 ? <EmptyState>조건에 맞는 할 일이 없습니다.</EmptyState> : items.map((item) => <article className={`record-card todo-card ${item.is_completed ? 'completed' : ''}`} key={item.id}><div className="todo-title"><input aria-label={`${item.title} 완료 상태`} type="checkbox" checked={item.is_completed} onChange={() => toggle(item)} /><h3>{item.title}</h3></div><div className="record-meta"><span className={`badge ${item.is_public ? 'public' : ''}`}>{item.is_public ? '공개' : '비공개'}</span><span>{item.is_completed ? `완료 ${formatDate(item.completed_at)}` : '진행 중'}</span></div><p className="updated-at">수정: {formatDate(item.updated_at)}</p><div className="button-row"><button className="secondary-button" onClick={() => { setEditingId(item.id); setForm({ title: item.title, is_public: item.is_public }); window.scrollTo({ top: 0, behavior: 'smooth' }) }}>수정</button><button className="danger-button" onClick={() => remove(item)}>삭제</button></div></article>)}</div>
      </div>
    </section>
  )
}
