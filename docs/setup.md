# BuildLog 개발 환경 준비

## 1. 문서 상태

이 문서는 Phase 0에서 확인한 개발 환경과 Phase 1 이후에 사용할 설정을 기록합니다.

- 확인 날짜: 2026-10-26
- 현재 단계: Phase 2 React 프론트엔드와 Phase 3 SQLite 데이터 계층 완료
- 패키지 설치: FastAPI, React, 테스트 도구, SQLAlchemy와 Alembic 설치 완료
- 애플리케이션 코드 생성: FastAPI 기본 구조, React 기본 화면과 SQLite 데이터 계층 생성 완료
- 데이터베이스 생성: `database/buildlog.sqlite3` 생성 완료, Git 제외 대상
- Git 저장소: 초기화되어 있으며 기존 커밋과 원격 저장소 설정을 유지함

### Phase 0 결과

- 기능 범위를 `PRD.md`와 `spec.md` 기준으로 맞췄습니다.
- `mvp.md`에 남아 있던 이전 기능 범위 충돌을 제거했습니다.
- FastAPI, React와 SQLite의 현재 역할을 문서에서 통일했습니다. Supabase 연결은 관련 수업 이후로 보류했습니다.
- 현재 Python, SQLite, Node.js와 npm 환경으로 다음 Phase를 시작할 수 있습니다.
- 개발을 막는 항목은 없습니다.
- 다음 작업은 Phase 1의 FastAPI 백엔드 뼈대 만들기입니다.

### Phase 1 결과

- 프로젝트 공통 `.venv`를 만들고 고정된 백엔드 기본 패키지를 설치했습니다.
- FastAPI 애플리케이션, 설정 모듈, CORS와 공통 HTTP 오류 응답을 만들었습니다.
- `GET /api/health`와 FastAPI 자동 API 문서가 실제 서버에서 정상 응답했습니다.
- 상태 API, 허용 CORS, 차단 CORS와 공통 404 응답 테스트 4개가 통과했습니다.
- 설치된 패키지 의존성 검사에서 문제가 발견되지 않았습니다.
- 데이터베이스, 회원, 기록과 프론트엔드 기능은 아직 만들지 않았습니다.
- 다음 작업은 Phase 2의 React 프론트엔드 뼈대 만들기입니다.

### Phase 2 결과

- Vite로 React JavaScript 프로젝트를 만들고 패키지 버전을 `package-lock.json`에 기록했습니다.
- 공통 API 호출 함수가 `VITE_API_BASE_URL`을 읽어 FastAPI에 요청합니다.
- 첫 화면에서 `/api/health`의 연결 성공과 실패 상태를 쉬운 문장으로 보여줍니다.
- 휴대폰 화면에서도 사용할 수 있는 공통 레이아웃, 카드, 입력칸과 버튼 스타일을 준비했습니다.
- 프론트엔드 정적 검사, 화면 테스트 2개와 배포용 빌드가 통과했습니다.
- 실제 React와 FastAPI 개발 서버를 함께 실행해 화면, 상태 API와 CORS 응답을 확인했습니다.

### Phase 3 결과

- 백엔드의 SQLite 데이터 계층을 구현했습니다.
- SQLAlchemy 연결 엔진, 세션, 모델 공통 기반을 만들었습니다.
- SQLite 외래 키 검사를 연결할 때 자동으로 활성화합니다.
- Alembic 초기 변경 이력 `0001_initial`을 만들었습니다.
- 실제 SQLite 파일에서 Alembic 적용, 되돌리기와 재적용을 확인했습니다.
- 전체 백엔드 테스트 7개가 통과했습니다.
- Supabase 패키지, 연결 코드와 비밀 설정은 추가하지 않았습니다.
- 다음 작업은 Phase 4의 회원가입·로그인·닉네임 기능입니다.

## 2. 기술 구조

- 프론트엔드: React와 Vite, JavaScript
- 백엔드: Python과 FastAPI
- 데이터 접근: SQLAlchemy
- 데이터 구조 변경: Alembic
- 현재 개발·테스트 DB: SQLite
- 향후 서비스 DB: Supabase 수업 이후 별도 연결
- 백엔드 테스트: pytest
- 프론트엔드 테스트: Vitest와 Testing Library

현재는 SQLite만 사용합니다. Supabase는 관련 수업을 진행한 뒤 별도 작업으로 연결하며, 회원가입과 권한 처리는 계속 FastAPI가 담당합니다.

## 3. 현재 컴퓨터에서 확인한 도구

| 도구 | 확인한 버전 | 상태 |
| --- | --- | --- |
| Python | 3.13.14 | 사용 가능 |
| SQLite | 3.50.4 | Python 기본 모듈로 사용 가능 |
| pip | 26.1.2 | 사용 가능 |
| Node.js | 24.22.1 | 사용 가능 |
| npm | 11.19.1 | `npm.cmd`로 사용 가능 |
| FastAPI | 0.156.2 | `.venv`에 설치됨 |
| Uvicorn | 0.54.0 | `.venv`에 설치됨 |
| Pydantic Settings | 2.16.1 | `.venv`에 설치됨 |
| pytest | 9.1.1 | `.venv`에 설치됨 |
| HTTPX2 | 2.16.0 | `.venv`에 설치됨 |
| SQLAlchemy | 2.1.6 | `.venv`에 설치됨 |
| Alembic | 1.20.1 | `.venv`에 설치됨 |
| React | 19.3.1 | `frontend`에 설치됨 |
| Vite | 8.3.5 | `frontend`에 설치됨 |
| Vitest | 5.0.5 | `frontend`에 설치됨 |
| Testing Library React | 16.3.3 | `frontend`에 설치됨 |
| `.venv` | 있음 | Git 제외 대상 |
| `frontend/.env` | 있음 | 로컬 API 주소 설정, Git 제외 대상 |
| SQLite 파일 | `database/buildlog.sqlite3` | 생성 완료, Git 제외 대상 |

PowerShell의 실행 정책 때문에 `npm`을 직접 실행하면 `npm.ps1` 오류가 날 수 있습니다. 실행 정책을 바꾸지 않고 `npm.cmd`와 `npx.cmd`를 사용합니다.

## 4. 확인한 핵심 안정 버전

Phase 1과 Phase 2를 시작할 때 아래 버전을 기준으로 실제 설치 파일에 고정합니다.

| 항목 | 기준 버전 |
| --- | --- |
| FastAPI | 0.156.2 |
| Uvicorn | 0.54.0 |
| Pydantic Settings | 2.16.1 |
| HTTPX2 | 2.16.0 |
| React | 19.3.1 |
| Vite | 8.3.5 |
| Create Vite | 9.3.1 |
| Vite React 플러그인 | 6.1.2 |
| SQLAlchemy | 2.1.6 |
| Alembic | 1.20.1 |
| pytest | 9.1.1 |
| Vitest | 5.0.5 |
| Testing Library React | 16.3.3 |

현재 Node.js 24.22.1은 Vite가 요구하는 Node.js 범위를 충족합니다. 실제 설치 시 각 패키지의 호환 결과와 자동 테스트를 다시 확인하고 `requirements.txt`와 `package-lock.json`에 확정 버전을 기록합니다.

## 5. 개발 주소

| 대상 | 주소 |
| --- | --- |
| React 개발 서버 | `http://localhost:5173` |
| FastAPI 개발 서버 | `http://127.0.0.1:8000` |
| FastAPI API 문서 | `http://127.0.0.1:8000/docs` |
| FastAPI API 시작 경로 | `/api` |

FastAPI의 CORS 허용 목록에는 React 개발 주소를 정확히 등록합니다. 인증 정보를 사용하는 요청을 위해 모든 주소를 뜻하는 `*`는 사용하지 않습니다.

## 6. 환경 변수 이름

### 백엔드

| 이름 | 용도 | 개발 기본값 또는 입력 시점 |
| --- | --- | --- |
| `APP_ENV` | 실행 환경 구분 | 개발에서는 `development` |
| `DATABASE_URL` | 현재 실행 DB 연결 | 기본값은 내부 SQLite 파일 |
| `TEST_DATABASE_URL` | 자동 테스트 DB 연결 | 임시 SQLite 사용 |
| `AUTH_SECRET_KEY` | 로그인 토큰 서명 | Phase 4에서 안전한 임의 값 생성 |
| `FRONTEND_ORIGIN` | 허용할 React 주소 | `http://localhost:5173` |

### 프론트엔드

| 이름 | 용도 | 개발 기본값 |
| --- | --- | --- |
| `VITE_API_BASE_URL` | FastAPI 기본 주소 | `http://127.0.0.1:8000/api` |

실제 값은 `.env`에 두며 Git에 기록하지 않습니다. `.env.example`에는 변수 이름과 비밀값이 아닌 예시만 기록합니다. `VITE_`로 시작하는 값은 브라우저에서 볼 수 있으므로 Supabase 연결 문자열이나 비밀번호를 넣지 않습니다.

## 7. 데이터베이스 사용 기준

### SQLite

- 로컬 개발과 자동 테스트에 사용합니다.
- 자동 테스트는 서로 영향을 주지 않는 임시 DB를 사용합니다.
- 파일로 생성되는 SQLite DB는 Git에 기록하지 않습니다.
- Python에 포함된 `sqlite3` 모듈을 사용하며 현재 버전은 3.50.4입니다.

### Supabase PostgreSQL

- 현재 개발 범위에서는 연결하지 않습니다.
- Supabase 수업을 진행한 뒤 별도 작업으로 추가합니다.
- 그때에도 FastAPI 백엔드만 연결하고 비밀 연결 문자열은 `.env`에서 관리합니다.

## 8. Phase별 사용자 준비 사항

### Phase 0~2

사용자가 제공할 비밀값이나 외부 계정 설정은 없습니다.

### Phase 3 이후

현재 SQLite 사용에는 사용자가 준비할 값이 없습니다. Supabase 프로젝트와 연결 문자열은 관련 수업 이후 별도 요청이 있을 때만 준비합니다.

## 9. 설치와 실행 명령

### Phase 1에서 실행한 작업

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

### 백엔드 실행

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

### 백엔드 테스트

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m pytest
```

Phase 1에서는 FastAPI 기본 패키지를 설치했고 Phase 3에서 SQLAlchemy와 Alembic을 추가했습니다. PostgreSQL 드라이버와 인증 패키지는 아직 설치하지 않았습니다.

### SQLite 변경 이력 적용

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head
```

### SQLite 변경 이력 되돌리기

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m alembic -c alembic.ini downgrade base
```

### 프론트엔드 설치와 실행

```powershell
Set-Location frontend
npm.cmd install
Copy-Item .env.example .env
npm.cmd run dev
```

### 프론트엔드 확인

```powershell
Set-Location frontend
npm.cmd run lint
npm.cmd run test
npm.cmd run build
```

설치된 프론트엔드 패키지 버전은 `package-lock.json`에 고정되어 있습니다.

## 10. 공식 참고 문서

- FastAPI 릴리스: <https://fastapi.tiangolo.com/release-notes/>
- FastAPI CORS: <https://fastapi.tiangolo.com/tutorial/cors/>
- FastAPI 보안: <https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>
- React 버전: <https://react.dev/versions>
- Vite 시작 안내: <https://vite.dev/guide/>
- SQLAlchemy 데이터베이스 지원: <https://docs.sqlalchemy.org/en/21/dialects/>
- Supabase 데이터베이스: <https://supabase.com/docs/guides/database/overview>
- Supabase PostgreSQL 연결: <https://supabase.com/docs/guides/database/connecting-to-postgres>
