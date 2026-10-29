# 사빈의 채용 레이더 — 자동 배포 설정

기존 2024~2026 채용 레이더 v8을 포함합니다. **새 공고 자동 수집은 포함하지 않습니다.** 모집 상태는 접속 날짜를 기준으로 브라우저에서 계산합니다.

## 최초 1회 설정

1. GitHub에서 `sabin-career-radar` 새 저장소를 만듭니다. 공개(public) 또는 비공개(private) 저장소를 선택할 수 있습니다.
2. 저장소의 **Add file → Upload files**에서 이 폴더 안의 `index.html`, `netlify.toml`, `.gitignore`, `README.md`를 업로드하고 **Commit changes**를 누릅니다. (ZIP 파일 그대로 올리는 것이 아닙니다.)
3. 기존 Netlify 사이트 관리자에서 **Project configuration → Developer settings → Continuous deployment → Repository → Link repository**로 이동합니다.
4. GitHub 접근을 허용하고 위에서 만든 저장소를 선택합니다. 배포 브랜치 `main`, 게시 경로 `.`(점), 빌드 명령어는 비워둡니다.
5. 첫 배포가 `Published`가 되면 기존 Netlify 사이트 주소로 접속해 최신 내용이 보이는지 확인합니다.

## 이후 수정

- GitHub 저장소에서 `index.html`을 열고 연필 아이콘(**Edit this file**)을 눌러 변경한 뒤 **Commit changes**를 누르면 Netlify가 자동 배포합니다.
- ChatGPT에서 새 HTML 수정본을 받았다면 GitHub의 `index.html`을 그 내용으로 **교체해 커밋**해야 합니다. 이 채팅에서 수정했다고 GitHub에 자동 업로드되지는 않습니다.
- 배포 완료 후 브라우저를 새로고침합니다. 같은 Netlify 주소를 사용할 수 있습니다.

## 구분할 것

- **자동 배포:** GitHub에 변경사항이 저장될 때 사이트가 자동 갱신됩니다.
- **모집 상태 자동 표시:** 기존 공고의 날짜를 읽어 접속일 기준으로 표시합니다.
- **신규 공고 자동 수집:** 별도 데이터 수집·검증·등록 프로그램이 필요합니다. 이 배포에는 포함되지 않습니다.

Git 연동 공식 설명: https://docs.netlify.com/build/git-workflows/repo-permissions-linking/
