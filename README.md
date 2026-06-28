# HAFSQuiz

외대부고(한국외국어대학교 부속 외국어고등학교) 학내 전용 킬러 문항 퀴즈 플랫폼.

- **퀴즈 풀이** — 로그인 없이 누구나
- **퀴즈 생성** — `@hafs.hs.kr` 구글 계정 로그인 필요
- **AI 퀴즈 생성 가이드** — `/create` 상단에서 메모리 파일 다운로드 + 프롬프트 제공

## 기술 스택

| 항목 | 내용 |
|---|---|
| Backend | Python Flask |
| Auth | Google OAuth 2.0 (authlib) |
| 인프라 | OCI AMD 무료 인스턴스 + DuckDNS |
| 배포 | GitHub Actions → SSH deploy |

---

## 로컬 개발 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경변수 설정
cp .env.example .env
# .env 편집: SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# 3. 실행
python app.py
# → http://127.0.0.1:5001
```

> 로컬에서 Google OAuth 테스트 시 `http://localhost:5001/auth/callback`을 Google Cloud Console 리디렉션 URI에 추가해야 합니다.

---

## OCI 서버 최초 설정

```bash
# 1. 코드 클론
git clone https://github.com/inoyu4649/HAFSQuiz.git ~/HAFSQuiz
cd ~/HAFSQuiz

# 2. 자동 설치 스크립트 실행
bash deploy/setup.sh

# 3. 환경변수 설정
cp .env.example .env
nano .env   # SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET 입력

# 4. SSL 인증서 발급
sudo certbot --nginx -d hafsquiz.duckdns.org

# 5. 서비스 시작
sudo systemctl enable hafsquiz
sudo systemctl start hafsquiz
```

---

## GitHub Actions 자동 배포 설정

Push to `main` → OCI 서버 자동 배포.

### GitHub Secrets 등록

Repository → Settings → Secrets and variables → Actions → **New repository secret**

| Secret 이름 | 값 |
|---|---|
| `OCI_HOST` | OCI 퍼블릭 IP 또는 `hafsquiz.duckdns.org` |
| `OCI_USER` | SSH 유저명 (보통 `ubuntu` 또는 `opc`) |
| `OCI_SSH_KEY` | OCI 접속용 SSH **프라이빗** 키 전체 내용 |

### Google OAuth 설정

[Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials → OAuth 2.0 Client IDs

승인된 리디렉션 URI 추가:
```
https://hafsquiz.duckdns.org/auth/callback
```

---

## 퀴즈 파일 형식

퀴즈는 동일 이름의 HTML + JSON 쌍으로 구성됩니다.

```
quizzes/
├── science212danwon.html   ← 퀴즈 UI (테마 포함, JSON fetch)
└── science212danwon.json   ← 문항 데이터
```

**JSON 구조** (`<name>danwon.json`):
```json
{
  "meta": { "title": "외대부고 통합과학 천문학 킬러 50", "version": "1.0" },
  "questions": [
    {
      "id": 1,
      "question": "문제 본문",
      "choices": ["선지1", "선지2", "선지3", "선지4", "선지5"],
      "answer": 0,
      "explanation": "해설 (plain text, 마크다운 금지)"
    }
  ]
}
```

**테마** (3종):
- `history` — 한국사 갈색 다크
- `social` — 통합사회 노란 라이트  
- `science` — 통합과학 청록 다크

---

## Contributors

- **[inoyu4649](https://github.com/inoyu4649)**
- **Claude** (Anthropic Claude Code)
