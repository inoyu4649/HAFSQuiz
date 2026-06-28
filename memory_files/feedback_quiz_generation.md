---
name: feedback-quiz-generation
description: 퀴즈 문항 생성 시 지켜야 할 스타일·형식 규칙
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4d415f9a-97e5-48bb-8540-95833052b6c3
---

## 해설 스타일 — questions.json 기준

explanation(해설)은 questions.json의 방식을 따른다.

**Why:** 사용자가 기존 questions.json을 읽어 그 방식으로 쓰라고 명시적으로 요청하였다.

**How to apply:**

1. 마크다운 기호 금지 — **bold**, ## 헤더, 줄 앞 - 목록 기호 모두 사용하지 않는다.

2. 선지 번호는 ①②③④⑤ 기호 사용 — "1번", "2번" 형식이 아니라 원문자 기호를 그대로 쓴다.

3. 오답 라벨 형식 — 각 오답은 "③ 한두 단어 태그. 설명 본문." 형태로 작성한다.
   예: "③ 조약 치환. 청·일 동시 파병의 근거는 톈진 조약(1885)이다. '포츠머스 조약'은 러일전쟁 종전 조약으로 시기·당사국이 다르다."

4. 오답 구분 — 각 선지 설명은 \n으로 구분한다. 별도 문단 기호 없이 줄바꿈만 사용.

5. 정답 언급 방식 — "정답은 N번이다" 형식 사용하지 않는다. 첫 줄에 정답의 근거를 서술하거나, 오답들만 분석하는 것으로 충분하다.

6. 검증 — 생성 후 ** / ## / 줄 앞 - / "N번" 패턴이 없는지 확인한다.

## 정답 위치 균일 배분 (중요)

50문항 기준 정답 위치를 ①②③④⑤ 각 10개씩 균일하게 배분해야 한다.

**Why:** 초기 생성 시 정답이 ①(index 0)에 42/50 집중되었고, 사용자가 명시적으로 "1번 집중 현상을 피하기 위해 12345 균일하게 배분해줘"라고 요청하였다.

**How to apply:** 생성 직후 아래 Python 스크립트로 후처리한다. 선지 순서를 재배치하면서 해설 내 ①②③④⑤ 참조도 함께 갱신한다.

해설에서 선지 참조는 ①②③④⑤ 기호를 사용하므로, 스크립트도 그에 맞게 기호를 치환한다.

```python
import json, re, copy
from collections import Counter

CIRCLE = ['①', '②', '③', '④', '⑤']

def rearrange(q, target):
    q = copy.deepcopy(q)
    old_answer = q['answer']
    if old_answer == target:
        return q
    choices = q['choices']
    correct = choices[old_answer]
    wrong = [choices[i] for i in range(5) if i != old_answer]
    new_choices = wrong[:target] + [correct] + wrong[target:]
    wrong_old_indices = [i for i in range(5) if i != old_answer]
    old_to_new = {old_answer: target}
    for k, old_idx in enumerate(wrong_old_indices):
        old_to_new[old_idx] = k if k < target else k + 1
    # ①②③④⑤ 기호 치환 (해설이 원문자 기호를 사용하는 경우)
    pattern = '|'.join(re.escape(c) for c in CIRCLE)
    def sub_circle(m):
        old_n = CIRCLE.index(m.group(0))
        new_n = old_to_new.get(old_n, old_n)
        return CIRCLE[new_n]
    q['choices'] = new_choices
    q['answer'] = target
    q['explanation'] = re.sub(pattern, sub_circle, q['explanation'])
    return q

with open('파일명.json', encoding='utf-8') as f:
    data = json.load(f)
data['questions'] = [rearrange(q, i % 5) for i, q in enumerate(data['questions'])]
with open('파일명.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(sorted(Counter(q['answer'] for q in data['questions']).items()))
```

## 정답 위치를 설명에서 "정답은 N번이다" 표기 주의

"정답은 1번이다"처럼 고정 표기를 쓰면 선지 재배치 후 틀려진다. 대신 "정답은 (선지 내용)이다" 형태로 쓰거나, 재배치 스크립트가 자동 갱신할 수 있도록 "N번이다" 형식을 유지한다.
