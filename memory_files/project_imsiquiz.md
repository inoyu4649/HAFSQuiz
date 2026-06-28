---
name: project-imsiquiz
description: imsiquiz 프로젝트 개요 — 외대부고 한국사·통합사회 킬러 퀴즈 웹앱, 파일 구조, PDF 처리
metadata:
  node_type: memory
  type: project
  originSessionId: 4d415f9a-97e5-48bb-8540-95833052b6c3
---

외대부고(한국외국어대학교 부속 외국어고등학교) 내신 대비용 킬러 문항 퀴즈 웹앱. 한국사 + 통합사회 + 통합과학 파트 포함.

**Why:** 외대부고 출제위원 시뮬레이션 — PDF 교재에서 사료/지문을 추출해 단어/수치 하나를 비튼 5지선다 킬러 문항을 생성하고 브라우저에서 바로 풀 수 있도록 제공.

**How to apply:** 새 문항 세트나 HTML 페이지 추가 요청이 오면 [[reference-questions-json-format]]과 [[reference-quiz-html-format]] 기준을 먼저 확인한다.

## 파일 구조 (C:\Users\이민기\Desktop\개발\imsiquiz\)

### 한국사
- historyquiz.html         — 근대사 3단원 퀴즈 (관리자 없음, 다크 전용)
- history1danwon.html      — 전근대사 1단원 퀴즈
- history2danwon.html      — 전근대사 2단원 퀴즈
- questions.json           — 근대사 3단원 킬러 100문항 (historyquiz.html이 fetch)
- history1danwon.json      — 전근대사 1단원 문항
- history2danwon.json      — 전근대사 2단원 킬러 50문항

### 통합사회
- social31danwon.html      — 통합사회 3-1단원 기후 킬러 50문항 퀴즈 (온대·냉대·한대·건조, 열대 제외)
- social31danwon.json      — 통합사회 3-1단원 기후 50문항

### 통합과학
- science212danwon.html    — 통합과학 2단원 천문학(우주 형성) 킬러 50문항 퀴즈 (다크 진회색+청록 테마)
- science212danwon.json    — 통합과학 2단원 천문학 킬러 50문항 (빅뱅·스펙트럼·별의 진화·태양계 형성)
- science33danwon.html     — 통합과학 생명과학(유전) 킬러 50문항 퀴즈 (다크 진회색+청록 테마, prefix "hafs-science-danwon33-progress-v1")
- science33danwon.json     — 통합과학 생명과학 킬러 50문항 (핵산 구조·샤르가프·유전자-단백질-형질·전사/번역·코돈/유전부호)
- science31danwon.html     — 통합과학 지구과학(지권 3-1) 킬러 25문항 퀴즈 (다크 진회색+청록 테마, prefix "hafs-science-danwon31-progress-v1")
- science31danwon.json     — 통합과학 지구과학 킬러 25문항 (암석권/연약권·판 구조론·발산/보존/수렴 경계·히말라야/안데스/마리아나/산안드레아스·대륙판vs해양판·베게너 대륙이동설·외핵 S파)
- science221danwon.html    — 통합과학 지각구성(II-2-1, 자연의 구성 물질) 킬러 25문항 퀴즈 (다크 진회색+청록 테마, prefix "hafs-science-danwon221-progress-v1")
- science221danwon.json    — 통합과학 지각구성 킬러 25문항 (규산염 사면체 SiO4 -4전하·산소4 규소1 정사면체·결합구조 5종[독립형 감람석/단사슬 휘석/복사슬 각섬석/판상 흑운모/망상 석영·장석]·쪼개짐vs깨짐·화학적 풍화 저항[석영 최강 감람석 최약]·지각/우주/생명체 구성원소 질량비·규산염광물 전체 92%·8대원소 98%)

### 공통 도구
- poppler-26.02.0/         — PDF→이미지 변환 도구 (pdftoppm.exe 경로 아래)

## PDF 처리 도구

pdftoppm 경로: C:\Users\이민기\Desktop\개발\imsiquiz\poppler-26.02.0\Library\bin\pdftoppm.exe
한글 경로 문제로 PDF를 ASCII 경로(스크래치패드)에 복사한 뒤 변환해야 한다.
권장 옵션: -png -scale-to-y 1600 (본문 교재, 텍스트 가독성 확보) / -png -scale-to-y 1700 (워크북 손필기 식별용)
텍스트가 작은 페이지는 PIL로 상하 절반(55/45% overlap)으로 분할하거나 6타일(3행×2열)로 추가 분할하면 가독성이 크게 높아진다.
단일 이미지 읽기도 누적 이미지 수가 많으면 거부될 수 있으므로 세션 초반에 변환하는 것이 안전하다.
Read 도구 내장 PDF 변환기는 이미지 기반 PDF에서 실패하므로 반드시 poppler 직접 호출로 처리한다.

## 세트 명명 규칙

- 한국사: historyNdanwon.json + historyNdanwon.html, STORAGE_KEYS prefix "hafs-history-danwonN-progress-v1"
- 통합사회: socialXYdanwon.json + socialXYdanwon.html, STORAGE_KEYS prefix "hafs-social-danwonXY-progress-v1"
- 통합과학: scienceXYdanwon.json + scienceXYdanwon.html, STORAGE_KEYS prefix "hafs-science-danwonXY-progress-v1"
- 항상 JSON + HTML 쌍으로 생성하고 제목 3곳(title 태그, h1, meta.title)을 일치시킨다.
