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

### 다른 과목 — 별도 테마 미정

수학·영어 등 추가 과목의 테마는 사용자가 지정할 때까지 미정이다.

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
