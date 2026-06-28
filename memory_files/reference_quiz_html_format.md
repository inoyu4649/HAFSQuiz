---
name: reference-quiz-html-format
description: imsiquiz 퀴즈 HTML 파일 양식 — 새 퀴즈 페이지 생성 시 참조
metadata:
  node_type: memory
  type: reference
  originSessionId: 4d415f9a-97e5-48bb-8540-95833052b6c3
---

퀴즈 HTML 파일의 기준 템플릿은 history1danwon.html 이다.
JSON 파일(예: history1danwon.json)을 fetch해서 퀴즈를 구동한다.

## 주요 설계 원칙

- 관리자 기능 없음 (historyquiz.html과 달리 AdminManager 클래스 제거)
- 다크모드 전용: :root에 다크 변수 고정, color-scheme: dark
- localStorage는 진행 상태(progress) 키 하나만 사용
- JSON fetch 시 항상 { cache: "no-store" }

## 제목 일치 규칙 (중요)

HTML `<title>` 태그, `<h1 id="appTitle">` 기본 텍스트, JSON `meta.title` 세 곳이 반드시 일치해야 한다.
JS가 로드 후 h1을 meta.title로 덮어쓰므로, 세 곳 중 하나만 바꾸면 불일치가 생긴다.

## STORAGE_KEYS 구조

각 HTML 파일마다 고유한 키 prefix를 써야 캐시가 겹치지 않는다.

  historyquiz.html      → "hafs-history-progress-v1", "hafs-history-dark-v1", "hafs-history-admin-questions-v1"
  history1danwon.html   → "hafs-history-danwon1-progress-v1"
  history2danwon.html   → "hafs-history-danwon2-progress-v1"
  social31danwon.html   → "hafs-social-danwon31-progress-v1"
  science212danwon.html → "hafs-science-danwon212-progress-v1"

새 파일을 만들 때는 prefix를 반드시 다르게 설정한다.

## 과목별 CSS 테마 (중요)

과목마다 테마 색상을 다르게 적용한다. 새 과목 세트를 만들 때 해당 과목 테마 변수를 사용해야 한다.

### 한국사 — 갈색(브라운) 계열 다크 테마 (history*.html 적용)

  --bg: #17130F
  --card: #2A2119
  --border: #5C4A37
  --text: #EFE5D1
  --title: #FFF1D2
  --primary: #A63D2F
  --primary-hover: #C34B3C
  --success: #6FA57D
  --wrong: #D0776D
  --muted: #B8AA96
  --shadow: 0 12px 30px rgba(0,0,0,.28)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: dark
  body 배경 그라디언트: rgba(255,255,255,.34) / rgba(74,59,42,.035) / rgba(74,59,42,.025)

### 통합사회 — 노란(골드) 계열 라이트 테마 (social*.html 적용)

  --bg: #FFFBEA
  --card: #FFFFFF
  --border: #DABC00
  --text: #2C2200
  --title: #1A1400
  --primary: #B89000
  --primary-hover: #9A7800
  --success: #2E7D32
  --wrong: #C62828
  --muted: #7A6A00
  --shadow: 0 12px 30px rgba(180,150,0,.13)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(255,240,100,.25) / rgba(180,150,0,.06) / rgba(180,150,0,.04)

### 통합과학 — 다크 진회색 + 위험 화학물질 초록 + 청록 강조 (science*.html, 생성됨: science212danwon / science33danwon / science31danwon)

  --bg: #111413             /* 순수 검정 대신 짙은 진회색(그린 틴트 미세 포함) */
  --card: #1B1F1D           /* 다크 카드 */
  --border: #1F4D3A         /* 화학 실험실 느낌의 진한 초록 테두리 */
  --text: #D8E8D8           /* 연초록 틴트 밝은 텍스트 */
  --title: #EEFAEE          /* 거의 흰색 제목 */
  --primary: #00B5A0        /* 청록(teal/cyan) 강조색 */
  --primary-hover: #009D8C
  --success: #43A047        /* 초록 정답 */
  --wrong: #E53935          /* 빨강 오답 */
  --muted: #5A7A6A          /* 회녹색 뮤트 */
  --shadow: 0 12px 30px rgba(0,150,120,.18)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: dark
  body 배경 그라디언트: rgba(0,200,80,.15) / rgba(0,160,70,.06) / rgba(0,160,70,.04)
    → 좌상단에 위험 화학물질 감성 독성 초록 글로우, 격자선도 초록 틴트

  STORAGE_KEYS prefix: "hafs-science-danwonXY-progress-v1"
  파일 명명: scienceXYdanwon.json + scienceXYdanwon.html

### 수학 (alias: math) — 과학테마 기반, 다크 + 파랑 강조 (math*.html 적용)

  --bg: #0F1117
  --card: #181C26
  --border: #1A3A5C
  --text: #D0DCF0
  --title: #EEF4FF
  --primary: #2979FF
  --primary-hover: #1A5FD4
  --success: #43A047
  --wrong: #E53935
  --muted: #4A6080
  --shadow: 0 12px 30px rgba(0,80,200,.18)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: dark
  body 배경 그라디언트: rgba(0,100,255,.15) / rgba(0,80,200,.06) / rgba(0,80,200,.04)
    → 좌상단 파랑 글로우

  STORAGE_KEYS prefix: "hafs-math-danwonXY-progress-v1"
  파일 명명: mathXYdanwon.json + mathXYdanwon.html

### 영어 (alias: english) — 사회테마 기반, 라이트 + 파랑 강조 (english*.html 적용)

  --bg: #EEF4FF
  --card: #FFFFFF
  --border: #2979FF
  --text: #0A1A3A
  --title: #05102A
  --primary: #1565C0
  --primary-hover: #0D47A1
  --success: #2E7D32
  --wrong: #C62828
  --muted: #3A5A8A
  --shadow: 0 12px 30px rgba(25,80,200,.13)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(50,120,255,.20) / rgba(25,80,200,.06) / rgba(25,80,200,.04)

  STORAGE_KEYS prefix: "hafs-english-danwonXY-progress-v1"
  파일 명명: englishXYdanwon.json + englishXYdanwon.html

### 국어 (alias: korean) — 사회테마 기반, 라이트 + 빨강 강조 (korean*.html 적용)

  --bg: #FFF5F5
  --card: #FFFFFF
  --border: #E53935
  --text: #2C0000
  --title: #1A0000
  --primary: #C62828
  --primary-hover: #A31515
  --success: #2E7D32
  --wrong: #1565C0
  --muted: #7A3030
  --shadow: 0 12px 30px rgba(200,0,0,.13)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(255,50,50,.18) / rgba(200,0,0,.06) / rgba(200,0,0,.04)

  STORAGE_KEYS prefix: "hafs-korean-danwonXY-progress-v1"
  파일 명명: koreanXYdanwon.json + koreanXYdanwon.html

### 일본어 (alias: nihongo) — 사회테마 기반, 라이트 + 벚꽃 핑크 강조 (nihongo*.html 적용)

  --bg: #FFF5F8
  --card: #FFFFFF
  --border: #F06292
  --text: #2C0A1A
  --title: #1A0510
  --primary: #D81B60
  --primary-hover: #AD1457
  --success: #2E7D32
  --wrong: #C62828
  --muted: #8A4060
  --shadow: 0 12px 30px rgba(220,50,120,.13)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(255,100,160,.18) / rgba(220,50,120,.06) / rgba(220,50,120,.04)

  STORAGE_KEYS prefix: "hafs-nihongo-danwonXY-progress-v1"
  파일 명명: nihongoXYdanwon.json + nihongoXYdanwon.html

### 중국어 (alias: zhongwen) — 사회테마 기반, 라이트 + 빨강 primary + 노란 그라디언트 hint (zhongwen*.html 적용)
  배경은 약간 붉은 아이보리 (#FFF5F0). 오성홍기 감성.

  --bg: #FFF5F0
  --card: #FFF8F5
  --border: #C62828
  --text: #2C0800
  --title: #1A0400
  --primary: #B71C1C
  --primary-hover: #8B0000
  --success: #2E7D32
  --wrong: #E65100
  --muted: #7A3010
  --shadow: 0 12px 30px rgba(180,0,0,.15)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(255,200,0,.22) / rgba(180,0,0,.08) / rgba(180,0,0,.05)
    → 좌상단 노란 글로우(금색) + 전체 붉은 틴트

  STORAGE_KEYS prefix: "hafs-zhongwen-danwonXY-progress-v1"
  파일 명명: zhongwenXYdanwon.json + zhongwenXYdanwon.html

### 독일어 (alias: deutsch) — 과학테마 기반, 다크 + 빨강 primary + 노란 그라디언트 hint (deutsch*.html 적용)
  독일 국기(검정-빨강-노랑) 감성.

  --bg: #111010
  --card: #1A1818
  --border: #4A2000
  --text: #F0DCC8
  --title: #FFEED8
  --primary: #CC2200
  --primary-hover: #AA1800
  --success: #43A047
  --wrong: #E06000
  --muted: #5A4030
  --shadow: 0 12px 30px rgba(160,20,0,.20)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: dark
  body 배경 그라디언트: rgba(255,210,0,.14) / rgba(160,20,0,.07) / rgba(160,20,0,.04)
    → 좌상단 노란 글로우, 전체 빨간 다크 틴트

  STORAGE_KEYS prefix: "hafs-deutsch-danwonXY-progress-v1"
  파일 명명: deutschXYdanwon.json + deutschXYdanwon.html

### 프랑스어 (alias: francais) — 사회테마 기반, 라이트 + 파랑 primary + 빨간 그라디언트 hint (francais*.html 적용)
  프랑스 삼색기(파랑-흰색-빨강) 감성.

  --bg: #F5F6FF
  --card: #FFFFFF
  --border: #1A3A8A
  --text: #0A0A2C
  --title: #05051A
  --primary: #1A3A8A
  --primary-hover: #0D2460
  --success: #2E7D32
  --wrong: #C62828
  --muted: #3A3A7A
  --shadow: 0 12px 30px rgba(20,40,160,.13)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(30,60,220,.16) / rgba(200,0,0,.06) / rgba(200,0,0,.03)
    → 파랑 글로우 주 + 빨강 hint

  STORAGE_KEYS prefix: "hafs-francais-danwonXY-progress-v1"
  파일 명명: francaisXYdanwon.json + francaisXYdanwon.html

### 스페인어 (alias: espanol) — 사회테마 기반, 라이트 + 빨강 primary + 노란 그라디언트 hint (espanol*.html 적용)
  스페인 국기(빨강-노랑-빨강) 감성. 배경은 사회테마와 동일한 #FFFBEA.

  --bg: #FFFBEA
  --card: #FFFFFF
  --border: #CC2200
  --text: #2C0800
  --title: #1A0400
  --primary: #CC2200
  --primary-hover: #9A1500
  --success: #2E7D32
  --wrong: #B71C1C
  --muted: #7A3010
  --shadow: 0 12px 30px rgba(180,20,0,.13)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: light
  body 배경 그라디언트: rgba(255,210,0,.22) / rgba(180,20,0,.07) / rgba(180,20,0,.04)
    → 사회테마 배경(아이보리) + 노란 글로우 + 빨강 hint

  STORAGE_KEYS prefix: "hafs-espanol-danwonXY-progress-v1"
  파일 명명: espanolXYdanwon.json + espanolXYdanwon.html

### 정보 (alias: computer) — 과학테마 기반, 다크 무채색 CLI 감성 (computer*.html 적용)

  --bg: #0A0A0A
  --card: #141414
  --border: #333333
  --text: #C8C8C8
  --title: #F0F0F0
  --primary: #E0E0E0
  --primary-hover: #FFFFFF
  --success: #58A458
  --wrong: #D04040
  --muted: #555555
  --shadow: 0 12px 30px rgba(0,0,0,.40)
  --header-height: 64px
  --footer-height: 76px
  color-scheme: dark
  body 배경 그라디언트: rgba(255,255,255,.06) / rgba(200,200,200,.02) / rgba(200,200,200,.01)
    → 무채색, 최소 글로우, 격자선 흰색 틴트 → CLI/터미널 감성

  STORAGE_KEYS prefix: "hafs-computer-danwonXY-progress-v1"
  파일 명명: computerXYdanwon.json + computerXYdanwon.html

## HTML 구조 (body 내부)

  header.app-header
    div.header-inner > h1#appTitle
    div.progress-wrap > div.progress-track > div#progressBar + span#progressText

  main
    section#quizScreen.screen.active
      div.quiz-layout
        article.archive-card.question-card
          div.question-kicker > span#questionNumber + button#explanationButton
          p#questionText
          div#choices
          div#explanation
        aside.archive-card.navigator
          p.navigator-title
          div#numberGrid

    section#resultScreen.screen
      div.archive-card.result-panel
        div#resultScore + p#resultSummary
        div.result-actions
          button#reviewButton
          button#retryWrongButton
          button#restartButton.primary-button

  nav.footer-nav
    div.footer-inner
      button#previousButton
      button#submitButton.primary-button
      button#nextButton

## JS 클래스 구조

  QuizApp
    - originalQuestions, questions, currentIndex, answers, revealedQuestionIds, isSubmitted, reviewMode
    - loadQuestions()   fetch JSON → loadProgress() → renderQuestion()
    - shuffleQuestions()
    - renderQuestion()
    - selectChoice(index)  선택 시 즉시 해설 노출 (revealedQuestionIds에 추가)
    - next() / previous() / jumpTo(index)
    - submit()         채점 후 resultScreen 표시
    - showExplanation()
    - retryWrongAnswers()
    - reviewAnswers()
    - restart()        progress 삭제 후 재셔플
    - saveProgress() / loadProgress()   localStorage
    - renderNumberGrid()
    - escapeHTML(value)

  DOMContentLoaded
    new QuizApp() → loadQuestions()
    (AdminManager 없음)

## 선지 레이블

  const choiceLabels = ["①","②","③","④","⑤"]

## 반응형 브레이크포인트

  720px: quiz-layout 2열(문제+네비게이터), footer 3열
  1040px: 문제 영역 최대 760px 중앙 정렬
