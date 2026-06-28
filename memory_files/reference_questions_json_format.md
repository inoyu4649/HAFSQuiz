---
name: reference-questions-json-format
description: imsiquiz 프로젝트의 questions.json 양식 — 퀴즈 문항 생성 시 바로 참조
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4d415f9a-97e5-48bb-8540-95833052b6c3
---

questions.json 파일은 C:\Users\이민기\Desktop\개발\imsiquiz\ 에 위치한다.

## 최상위 구조

{
  "meta": {
    "title": "퀴즈 세트 제목",
    "version": "1.0"
  },
  "questions": [ ... ]
}

## 문항 객체 구조 (questions 배열의 각 요소)

{
  "id": 1,                          // 1부터 시작하는 정수
  "question": "문제 본문 텍스트",     // \n으로 줄바꿈, 사료/지문 포함 가능
  "choices": [                      // 반드시 5개 (5지선다)
    "선지1",
    "선지2",
    "선지3",
    "선지4",
    "선지5"
  ],
  "answer": 0,                      // 0-base 인덱스 (0~4)
  "explanation": "해설 텍스트"       // plain text만 사용, 마크다운 기호(**,#,-) 금지
}

## 규칙

- answer는 0-base: 첫 번째 선지가 정답이면 0, 두 번째면 1
- explanation에 마크다운 사용 금지 (** , ## , - 등)
- 해설에서 선지 번호는 ①②③④⑤ 기호로 표기 ("1번"/"2번" 형식 사용 금지)
- 각 오답은 "③ 한두 단어 라벨. 설명." 형태로 \n 구분 작성 — [[feedback-quiz-generation]] 참조
- question 내 사료/지문은 큰따옴표 또는 들여쓰기로 구분
- 기존 questions.json(근대사 100문항)을 덮어쓰지 말고 별도 파일로 저장

## 파일 명명 예시

- questions.json          — 근대사 킬러 100문항 (원본, 덮어쓰기 금지)
- history1danwon.json     — 전근대사 1단원
- history2danwon.json     — 전근대사 2단원 킬러 50문항
- social31danwon.json     — 통합사회 3-1단원 기후 킬러 50문항 (온대·냉대·한대·건조)
