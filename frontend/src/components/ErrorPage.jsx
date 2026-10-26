import { useEffect, useState } from 'react'
import { errorApi } from '../api/client.js'
import EmptyState from './EmptyState.jsx'

const blankForm = { title: '', content: '', solution: '', is_resolved: false, is_public: false }
const filters = [['all', '전체'], ['unresolved', '미해결'], ['resolved', '해결']]
const formatDate = (value) => value ? new Date(value).toLocaleString('ko-KR') : '-'

export default function ErrorPage({ token }) {
  const [items, setItems] = useState([])
  const [form, setForm] = useState(blankForm)
  const [editingId, setEditingId] = useState(null)
  const [filter, setFilter] = useState('all')
  const [query, setQuery] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = async (nextFilter = filter, search = query) => {
    setLoading(true); setError('')
    try { setItems(await errorApi.list(token, nextFilter, search)) }
    catch (requestError) { setError(requestError.message) }
    finally { setLoading(false) }
  }
  useEffect(() => {
    let active = true
    errorApi.list(token, filter, '')
      .then((records) => { if (active) setItems(records) })
      .catch((requestError) => { if (active) setError(requestError.message) })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [token, filter])

  const submit = async (event) => {
    event.preventDefault(); setError('')
    try {
      if (editingId) await errorApi.update(token, editingId, form)
      else await errorApi.create(token, { title: form.title, content: form.content, solution: form.solution, is_public: form.is_public })
      setForm(blankForm); setEditingId(null); await load()
    } catch (requestError) { setError(requestError.message) }
  }

  const edit = (item) => { setEditingId(item.id); setForm({ title: item.title, content: item.content, solution: item.solution ?? '', is_resolved: item.is_resolved, is_public: item.is_public }); window.scrollTo({ top: 0, behavior: 'smooth' }) }
  const remove = async (item) => { if (!window.confirm(`“${item.title}” 오류 기록을 삭제할까요? 삭제 후 되돌릴 수 없습니다.`)) return; try { await errorApi.remove(token, item.id); await load() } catch (e) { setError(e.message) } }

  return (
    <section className="page-section">
      <div className="page-heading"><div><p className="eyebrow">Phase 8</p><h1>오류 기록</h1><p>막혔던 원인과 해결 방법을 다음의 나를 위해 남겨보세요.</p></div></div>
      <div className="content-grid">
        <form className="panel stack-form editor-panel" onSubmit={submit}>
          <h2>{editingId ? '오류 기록 수정' : '새 오류 기록'}</h2>
          <label>오류 제목<input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} maxLength="100" required /></label>
          <label>오류 내용<textarea value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} maxLength="5000" rows="6" required /></label>
          <label>해결 방법<textarea value={form.solution} onChange={(e) => setForm({ ...form, solution: e.target.value })} maxLength="5000" rows="5" placeholder="아직 해결하지 못했다면 비워두세요." /></label>
          {editingId && <label className="check-label"><input type="checkbox" checked={form.is_resolved} onChange={(e) => setForm({ ...form, is_resolved: e.target.checked })} />해결 완료</label>}
          <label className="check-label"><input type="checkbox" checked={form.is_public} onChange={(e) => setForm({ ...form, is_public: e.target.checked })} />공개 기록으로 저장</label>
          {error && <p className="message error-message">{error}</p>}
          <div className="button-row"><button className="primary-button">{editingId ? '수정 저장' : '오류 저장'}</button>{editingId && <button type="button" className="secondary-button" onClick={() => { setEditingId(null); setForm(blankForm) }}>수정 취소</button>}</div>
        </form>
        <div className="list-column">
          <div className="segmented filter-row">{filters.map(([value, label]) => <button key={value} className={filter === value ? 'active' : ''} onClick={() => { setLoading(true); setFilter(value) }}>{label}</button>)}</div>
          <form className="search-row" onSubmit={(e) => { e.preventDefault(); load(filter, query) }}><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="오류 제목이나 내용 검색" /><button className="secondary-button">검색</button></form>
          {loading ? <EmptyState>오류 기록을 불러오는 중입니다.</EmptyState> : items.length === 0 ? <EmptyState>조건에 맞는 오류 기록이 없습니다.</EmptyState> : items.map((item) => <article className="record-card" key={item.id}><div className="record-meta"><span className={`badge ${item.is_resolved ? 'resolved' : 'unresolved'}`}>{item.is_resolved ? '해결' : '미해결'}</span><span className={`badge ${item.is_public ? 'public' : ''}`}>{item.is_public ? '공개' : '비공개'}</span><time>{formatDate(item.created_at)}</time></div><h3>{item.title}</h3><h4>오류 내용</h4><p className="record-content">{item.content}</p><h4>해결 방법</h4><p className="record-content">{item.solution || '아직 해결 방법이 없습니다.'}</p>{item.is_resolved && <p className="updated-at">해결: {formatDate(item.resolved_at)}</p>}<p className="updated-at">수정: {formatDate(item.updated_at)}</p><div className="button-row"><button className="secondary-button" onClick={() => edit(item)}>수정·해결</button><button className="danger-button" onClick={() => remove(item)}>삭제</button></div></article>)}
        </div>
      </div>
    </section>
  )
}
