# 사빈의 채용 레이더 — 자동 공고 추가

기존 46건의 채용 이력을 유지하면서 고용24 **공채속보**에 올라온 관련 공고를 매일 검색하여 `data/auto_jobs.json`에 중복 없이 저장하고 Netlify를 자동 재배포합니다.

## 필요한 초기 설정

1. 이 저장소 파일을 GitHub `rohawedding0-debug/Sabin-Hong`에 **폴더 구조를 유지해** 업로드합니다 (`.github/workflows/daily-jobs.yml`, `scripts/sync_jobs.py`, `data/auto_jobs.json`, `index.html`).
2. 고용24 **기업회원용 OPEN API**를 신청하여 **공채속보** 이용 승인을 받고 인증키를 발급받습니다. 이용 요건 확인: https://www.work24.go.kr/cm/e/a/0110/selectOpenApiIntro.do
3. GitHub 저장소 → **Settings → Secrets and variables → Actions → New repository secret** 에서 이름을 `WORK24_API_KEY`로 지정하고 키를 저장합니다. **공개 파일이나 채팅에 키를 적지 마세요.**
4. GitHub **Actions → 매일 채용공고 자동 확인 → Run workflow** 로 첫 실행을 테스트합니다. 문제가 없으면 매일 한국시간 오전 9시 20분쯤 자동으로 실행됩니다(실제 실행은 GitHub 스케줄에 따라 지연 가능).
5. Netlify 프로젝트가 같은 GitHub 저장소의 `main` 브랜치에 연결되어 있어야 수정된 데이터가 자동으로 사이트에 배포됩니다.

## 기능과 제한

- 모집 분야: 소재·화학 R&D, 생산·공정 기술, 제조 데이터·DX, ESG·환경 데이터.
- 범위: 고용24 공채속보의 **대기업(10)·중견기업(40)** 및 **정규직(10)** 목록. 신입과 경력 모두 확인.
- 채용연계형 인턴·영업 등 제외. 키워드 기반 분류로 오분류가 있을 수 있으며, 실제 지원 가능 여부는 공고 원문 확인.
- 공고 제목과 모집 기간, 기업명, 공식 채용 링크만 자동 수집. 상세 JD·필수 경력·회사 평균연봉은 추정하지 않음.
- 이미 있던 46건은 삭제하지 않음. 365일 이내 마감된 자동 발견 공고는 이력으로 보관.
- **자소설닷컴 직접 수집은 포함하지 않음**. 공식 접근 권한과 안정적인 API가 확인될 때 연결 가능.
- 등록된 인증키가 없으면 기존 사이트는 작동하지만 신규 공고 자동 수집은 실행되지 않음.

공식 문서: https://www.work24.go.kr/cm/e/a/0110/selectOpenApiSvcInfo.do?fullApiSvcId=000000000000000000000000000000%5E000000000000000000000000000079
