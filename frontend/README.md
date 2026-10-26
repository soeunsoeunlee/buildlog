# BuildLog 프론트엔드

React와 Vite로 만든 BuildLog 화면입니다. 회원가입·로그인·닉네임 변경과 공부 기록, 할 일, 오류 기록의 개인 관리 기능을 제공합니다.

공개 기록 모아보기, 댓글, 좋아요와 신고는 아직 구현하지 않았습니다.

## 실행

```powershell
npm.cmd install
Copy-Item .env.example .env
npm.cmd run dev
```

기본 주소는 `http://localhost:5173`입니다. 백엔드 API 주소를 바꾸려면 `.env.example`을 참고해 실제 `.env`에 `VITE_API_BASE_URL`을 설정합니다.

## 확인

```powershell
npm.cmd run lint
npm.cmd run test
npm.cmd run build
```
