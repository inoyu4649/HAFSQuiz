import os
import json
import re
import html as html_module
from pathlib import Path
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, send_from_directory, jsonify, abort, Response
)
from authlib.integrations.flask_client import OAuth
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

QUIZ_DIR = Path(__file__).parent / 'quizzes'
QUIZ_DIR.mkdir(exist_ok=True)

MEMORY_DIR = Path(__file__).parent / 'memory_files'

ALLOWED_DOMAIN = 'hafs.hs.kr'

MEMORY_FILES = [
    ('project_imsiquiz.md', '프로젝트 개요'),
    ('reference_questions_json_format.md', 'JSON 양식'),
    ('reference_quiz_html_format.md', 'HTML 양식'),
    ('feedback_quiz_generation.md', '문항 생성 규칙'),
]

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

THEMES = {
    'history': {
        'label': '한국사 (갈색 다크)',
        'bg': '#17130F',
        'card': '#2A2119',
        'border': '#5C4A37',
        'text': '#EFE5D1',
        'title_color': '#FFF1D2',
        'primary': '#A63D2F',
        'primary_hover': '#C34B3C',
        'success': '#6FA57D',
        'wrong': '#D0776D',
        'muted': '#B8AA96',
        'shadow': '0 12px 30px rgba(0,0,0,.28)',
        'color_scheme': 'dark',
        'radial_color': 'rgba(255,255,255,.34)',
        'grid_h': 'rgba(74,59,42,.035)',
        'grid_v': 'rgba(74,59,42,.025)',
        'card_gradient_color': 'rgba(163,61,47,.08)',
        'primary_btn_text': '#FFF1D2',
        'num_current_text': '#17130F',
    },
    'social': {
        'label': '통합사회 (노란 라이트)',
        'bg': '#FFFBEA',
        'card': '#FFFFFF',
        'border': '#DABC00',
        'text': '#2C2200',
        'title_color': '#1A1400',
        'primary': '#B89000',
        'primary_hover': '#9A7800',
        'success': '#2E7D32',
        'wrong': '#C62828',
        'muted': '#7A6A00',
        'shadow': '0 12px 30px rgba(180,150,0,.13)',
        'color_scheme': 'light',
        'radial_color': 'rgba(255,240,100,.25)',
        'grid_h': 'rgba(180,150,0,.06)',
        'grid_v': 'rgba(180,150,0,.04)',
        'card_gradient_color': 'rgba(184,144,0,.08)',
        'primary_btn_text': '#1A1400',
        'num_current_text': '#1A1400',
    },
    'science': {
        'label': '통합과학 (청록 다크)',
        'bg': '#111413',
        'card': '#1B1F1D',
        'border': '#1F4D3A',
        'text': '#D8E8D8',
        'title_color': '#EEFAEE',
        'primary': '#00B5A0',
        'primary_hover': '#009D8C',
        'success': '#43A047',
        'wrong': '#E53935',
        'muted': '#5A7A6A',
        'shadow': '0 12px 30px rgba(0,150,120,.18)',
        'color_scheme': 'dark',
        'radial_color': 'rgba(0,200,80,.15)',
        'grid_h': 'rgba(0,160,70,.06)',
        'grid_v': 'rgba(0,160,70,.04)',
        'card_gradient_color': 'rgba(0,181,160,.08)',
        'primary_btn_text': '#06120E',
        'num_current_text': '#06120E',
    },
    'math': {
        'label': '수학 (파랑 다크)',
        'bg': '#0F1117',
        'card': '#181C26',
        'border': '#1A3A5C',
        'text': '#D0DCF0',
        'title_color': '#EEF4FF',
        'primary': '#2979FF',
        'primary_hover': '#1A5FD4',
        'success': '#43A047',
        'wrong': '#E53935',
        'muted': '#4A6080',
        'shadow': '0 12px 30px rgba(0,80,200,.18)',
        'color_scheme': 'dark',
        'radial_color': 'rgba(0,100,255,.15)',
        'grid_h': 'rgba(0,80,200,.06)',
        'grid_v': 'rgba(0,80,200,.04)',
        'card_gradient_color': 'rgba(41,121,255,.08)',
        'primary_btn_text': '#EEF4FF',
        'num_current_text': '#0F1117',
    },
    'english': {
        'label': '영어 (파랑 라이트)',
        'bg': '#EEF4FF',
        'card': '#FFFFFF',
        'border': '#2979FF',
        'text': '#0A1A3A',
        'title_color': '#05102A',
        'primary': '#1565C0',
        'primary_hover': '#0D47A1',
        'success': '#2E7D32',
        'wrong': '#C62828',
        'muted': '#3A5A8A',
        'shadow': '0 12px 30px rgba(25,80,200,.13)',
        'color_scheme': 'light',
        'radial_color': 'rgba(50,120,255,.20)',
        'grid_h': 'rgba(25,80,200,.06)',
        'grid_v': 'rgba(25,80,200,.04)',
        'card_gradient_color': 'rgba(21,101,192,.08)',
        'primary_btn_text': '#FFFFFF',
        'num_current_text': '#05102A',
    },
    'korean': {
        'label': '국어 (빨강 라이트)',
        'bg': '#FFF5F5',
        'card': '#FFFFFF',
        'border': '#E53935',
        'text': '#2C0000',
        'title_color': '#1A0000',
        'primary': '#C62828',
        'primary_hover': '#A31515',
        'success': '#2E7D32',
        'wrong': '#1565C0',
        'muted': '#7A3030',
        'shadow': '0 12px 30px rgba(200,0,0,.13)',
        'color_scheme': 'light',
        'radial_color': 'rgba(255,50,50,.18)',
        'grid_h': 'rgba(200,0,0,.06)',
        'grid_v': 'rgba(200,0,0,.04)',
        'card_gradient_color': 'rgba(198,40,40,.08)',
        'primary_btn_text': '#FFFFFF',
        'num_current_text': '#1A0000',
    },
    'nihongo': {
        'label': '일본어 (핑크 라이트)',
        'bg': '#FFF5F8',
        'card': '#FFFFFF',
        'border': '#F06292',
        'text': '#2C0A1A',
        'title_color': '#1A0510',
        'primary': '#D81B60',
        'primary_hover': '#AD1457',
        'success': '#2E7D32',
        'wrong': '#C62828',
        'muted': '#8A4060',
        'shadow': '0 12px 30px rgba(220,50,120,.13)',
        'color_scheme': 'light',
        'radial_color': 'rgba(255,100,160,.18)',
        'grid_h': 'rgba(220,50,120,.06)',
        'grid_v': 'rgba(220,50,120,.04)',
        'card_gradient_color': 'rgba(216,27,96,.08)',
        'primary_btn_text': '#FFFFFF',
        'num_current_text': '#1A0510',
    },
    'zhongwen': {
        'label': '중국어 (홍기 라이트)',
        'bg': '#FFF5F0',
        'card': '#FFF8F5',
        'border': '#C62828',
        'text': '#2C0800',
        'title_color': '#1A0400',
        'primary': '#B71C1C',
        'primary_hover': '#8B0000',
        'success': '#2E7D32',
        'wrong': '#E65100',
        'muted': '#7A3010',
        'shadow': '0 12px 30px rgba(180,0,0,.15)',
        'color_scheme': 'light',
        'radial_color': 'rgba(255,200,0,.22)',
        'grid_h': 'rgba(180,0,0,.08)',
        'grid_v': 'rgba(180,0,0,.05)',
        'card_gradient_color': 'rgba(183,28,28,.08)',
        'primary_btn_text': '#FFFFFF',
        'num_current_text': '#1A0400',
    },
    'deutsch': {
        'label': '독일어 (독일기 다크)',
        'bg': '#111010',
        'card': '#1A1818',
        'border': '#4A2000',
        'text': '#F0DCC8',
        'title_color': '#FFEED8',
        'primary': '#CC2200',
        'primary_hover': '#AA1800',
        'success': '#43A047',
        'wrong': '#E06000',
        'muted': '#5A4030',
        'shadow': '0 12px 30px rgba(160,20,0,.20)',
        'color_scheme': 'dark',
        'radial_color': 'rgba(255,210,0,.14)',
        'grid_h': 'rgba(160,20,0,.07)',
        'grid_v': 'rgba(160,20,0,.04)',
        'card_gradient_color': 'rgba(204,34,0,.08)',
        'primary_btn_text': '#FFEED8',
        'num_current_text': '#111010',
    },
    'francais': {
        'label': '프랑스어 (삼색기 라이트)',
        'bg': '#F5F6FF',
        'card': '#FFFFFF',
        'border': '#1A3A8A',
        'text': '#0A0A2C',
        'title_color': '#05051A',
        'primary': '#1A3A8A',
        'primary_hover': '#0D2460',
        'success': '#2E7D32',
        'wrong': '#C62828',
        'muted': '#3A3A7A',
        'shadow': '0 12px 30px rgba(20,40,160,.13)',
        'color_scheme': 'light',
        'radial_color': 'rgba(30,60,220,.16)',
        'grid_h': 'rgba(200,0,0,.06)',
        'grid_v': 'rgba(200,0,0,.03)',
        'card_gradient_color': 'rgba(26,58,138,.08)',
        'primary_btn_text': '#FFFFFF',
        'num_current_text': '#05051A',
    },
    'espanol': {
        'label': '스페인어 (국기 라이트)',
        'bg': '#FFFBEA',
        'card': '#FFFFFF',
        'border': '#CC2200',
        'text': '#2C0800',
        'title_color': '#1A0400',
        'primary': '#CC2200',
        'primary_hover': '#9A1500',
        'success': '#2E7D32',
        'wrong': '#B71C1C',
        'muted': '#7A3010',
        'shadow': '0 12px 30px rgba(180,20,0,.13)',
        'color_scheme': 'light',
        'radial_color': 'rgba(255,210,0,.22)',
        'grid_h': 'rgba(180,20,0,.07)',
        'grid_v': 'rgba(180,20,0,.04)',
        'card_gradient_color': 'rgba(204,34,0,.08)',
        'primary_btn_text': '#FFFFFF',
        'num_current_text': '#1A0400',
    },
    'computer': {
        'label': '정보 (CLI 다크)',
        'bg': '#0A0A0A',
        'card': '#141414',
        'border': '#333333',
        'text': '#C8C8C8',
        'title_color': '#F0F0F0',
        'primary': '#E0E0E0',
        'primary_hover': '#FFFFFF',
        'success': '#58A458',
        'wrong': '#D04040',
        'muted': '#555555',
        'shadow': '0 12px 30px rgba(0,0,0,.40)',
        'color_scheme': 'dark',
        'radial_color': 'rgba(255,255,255,.06)',
        'grid_h': 'rgba(200,200,200,.02)',
        'grid_v': 'rgba(200,200,200,.01)',
        'card_gradient_color': 'rgba(224,224,224,.04)',
        'primary_btn_text': '#0A0A0A',
        'num_current_text': '#0A0A0A',
    },
}


STATIC_VER = '20250629c'


@app.context_processor
def inject_static_ver():
    return {'sv': STATIC_VER}


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            session['next'] = request.url
            return redirect(url_for('auth_login'))
        return f(*args, **kwargs)
    return decorated


def sanitize_name(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '', name)


def derive_storage_key(filename_base: str) -> str:
    name = filename_base
    if name.endswith('danwon'):
        name = name[:-6]
    for prefix in ('history', 'social', 'science', 'math', 'english', 'korean',
                   'nihongo', 'zhongwen', 'deutsch', 'francais', 'espanol', 'computer'):
        if name.lower().startswith(prefix):
            rest = name[len(prefix):]
            return f'hafs-{prefix}-danwon{rest}-progress-v1'
    return f'hafs-quiz-{name}-progress-v1'


def generate_quiz_html(filename_base: str, title: str, theme_key: str) -> str:
    t = THEMES[theme_key]
    storage_key = derive_storage_key(filename_base)
    json_file = filename_base + '.json'
    esc_title = html_module.escape(title)

    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc_title}</title>
  <style>
    :root {{
      --bg: {t['bg']};
      --card: {t['card']};
      --border: {t['border']};
      --text: {t['text']};
      --title: {t['title_color']};
      --primary: {t['primary']};
      --primary-hover: {t['primary_hover']};
      --success: {t['success']};
      --wrong: {t['wrong']};
      --muted: {t['muted']};
      --shadow: {t['shadow']};
      --header-height: 64px;
      --footer-height: 76px;
      color-scheme: {t['color_scheme']};
    }}

    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}

    body {{
      margin: 0;
      min-width: 320px;
      min-height: 100vh;
      color: var(--text);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.65;
      background:
        radial-gradient(circle at 20% 10%, {t['radial_color']}, transparent 24rem),
        linear-gradient(90deg, {t['grid_h']} 1px, transparent 1px),
        linear-gradient(0deg, {t['grid_v']} 1px, transparent 1px),
        var(--bg);
      background-size: auto, 18px 18px, 18px 18px, auto;
    }}

    button, input, textarea, select {{ font: inherit; color: inherit; }}

    button {{
      min-height: 44px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--card);
      cursor: pointer;
      transition: transform .12s ease, background-color .12s ease, border-color .12s ease;
      touch-action: manipulation;
    }}

    button:hover {{ border-color: var(--primary); }}
    button:active {{ transform: translateY(1px); }}
    button:focus-visible {{
      outline: 3px solid color-mix(in srgb, var(--primary) 34%, transparent);
      outline-offset: 2px;
    }}

    .app-header {{
      position: sticky;
      top: 0;
      z-index: 10;
      min-height: calc(var(--header-height) + env(safe-area-inset-top));
      padding: calc(10px + env(safe-area-inset-top)) 14px 10px;
      border-bottom: 1px solid var(--border);
      background: color-mix(in srgb, var(--bg) 90%, transparent);
      backdrop-filter: blur(12px);
    }}

    .header-inner {{
      display: flex;
      align-items: center;
      max-width: 1120px;
      margin: 0 auto;
    }}

    h1 {{
      margin: 0;
      color: var(--title);
      font-size: 1rem;
      line-height: 1.25;
    }}

    .progress-wrap {{
      max-width: 1120px;
      margin: 10px auto 0;
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 10px;
      font-size: .86rem;
      color: var(--muted);
    }}

    .progress-track {{
      height: 9px;
      overflow: hidden;
      border: 1px solid var(--border);
      border-radius: 999px;
      background: color-mix(in srgb, var(--card) 70%, var(--bg));
    }}

    .progress-bar {{
      width: 0%;
      height: 100%;
      border-radius: inherit;
      background: var(--primary);
      transition: width .2s ease;
    }}

    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 16px 14px calc(var(--footer-height) + 26px + env(safe-area-inset-bottom));
    }}

    .screen {{ display: none; }}
    .screen.active {{ display: block; }}

    .quiz-layout {{ display: grid; gap: 14px; }}

    .archive-card {{
      border: 1px solid var(--border);
      border-radius: 8px;
      background:
        linear-gradient(145deg, {t['card_gradient_color']}, transparent 42%),
        var(--card);
      box-shadow: var(--shadow);
    }}

    .question-card {{ padding: 18px; }}

    .question-kicker {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 12px;
      color: var(--muted);
      font-size: .9rem;
    }}

    .question-text {{
      margin: 0 0 16px;
      color: var(--title);
      font-size: 1.08rem;
      font-weight: 750;
      white-space: pre-wrap;
      word-break: keep-all;
    }}

    .choices {{ display: grid; gap: 10px; }}

    .choice {{
      display: grid;
      grid-template-columns: 32px 1fr;
      gap: 10px;
      width: 100%;
      min-height: 54px;
      padding: 12px;
      text-align: left;
      background: color-mix(in srgb, var(--card) 88%, var(--bg));
    }}

    .choice .mark {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      border: 1px solid var(--border);
      border-radius: 50%;
      color: var(--title);
      font-weight: 800;
    }}

    .choice.selected {{ border-color: var(--primary); background: color-mix(in srgb, var(--primary) 14%, var(--card)); }}
    .choice.correct {{ border-color: var(--success); background: color-mix(in srgb, var(--success) 18%, var(--card)); }}
    .choice.wrong {{ border-color: var(--wrong); background: color-mix(in srgb, var(--wrong) 16%, var(--card)); }}

    .explanation {{
      display: none;
      margin-top: 16px;
      padding: 14px;
      border: 1px dashed var(--border);
      border-radius: 8px;
      white-space: pre-wrap;
      background: color-mix(in srgb, var(--bg) 52%, var(--card));
    }}

    .explanation.visible {{ display: block; }}

    .navigator {{ padding: 12px; }}

    .navigator-title {{ margin: 0 0 10px; color: var(--title); font-size: .95rem; font-weight: 800; }}

    .number-grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 7px; }}

    .number-grid button {{ min-height: 40px; padding: 0; font-size: .86rem; }}

    .number-grid button.current {{
      color: {t['num_current_text']};
      border-color: var(--primary);
      background: var(--primary);
    }}

    .number-grid button.answered {{ border-color: color-mix(in srgb, var(--success) 60%, var(--border)); }}

    .footer-nav {{
      position: fixed;
      left: 0; right: 0; bottom: 0;
      z-index: 12;
      padding: 10px 14px calc(10px + env(safe-area-inset-bottom));
      border-top: 1px solid var(--border);
      background: color-mix(in srgb, var(--bg) 92%, transparent);
      backdrop-filter: blur(12px);
    }}

    .footer-inner {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      max-width: 720px;
      margin: 0 auto;
    }}

    .primary-button {{
      color: {t['primary_btn_text']};
      border-color: var(--primary);
      background: var(--primary);
      font-weight: 800;
    }}

    .primary-button:hover {{ background: var(--primary-hover); }}
    .ghost-button {{ background: transparent; }}

    .result-panel {{ max-width: 760px; margin: 18px auto; padding: 22px; }}

    .result-score {{ margin: 8px 0 14px; color: var(--title); font-size: 2.25rem; font-weight: 900; line-height: 1.1; }}

    .result-actions {{ display: grid; gap: 10px; margin-top: 16px; }}

    @media (min-width: 720px) {{
      h1 {{ font-size: 1.15rem; }}
      main {{ padding-top: 22px; }}
      .quiz-layout {{ grid-template-columns: minmax(0, 1fr) 240px; align-items: start; }}
      .navigator {{ position: sticky; top: calc(var(--header-height) + 18px); }}
      .number-grid {{ grid-template-columns: repeat(4, 1fr); }}
      .footer-inner {{ grid-template-columns: 160px 1fr 160px; }}
    }}

    @media (min-width: 1040px) {{
      .quiz-layout {{ grid-template-columns: minmax(0, 760px) 260px; justify-content: center; }}
      .question-card {{ padding: 24px; }}
      .question-text {{ font-size: 1.16rem; }}
    }}
  </style>
</head>
<body>
  <header class="app-header">
    <div class="header-inner">
      <h1 id="appTitle">{esc_title}</h1>
    </div>
    <div class="progress-wrap" aria-live="polite">
      <div class="progress-track" aria-label="진행률"><div id="progressBar" class="progress-bar"></div></div>
      <span id="progressText">0 / 0</span>
    </div>
  </header>

  <main>
    <section id="quizScreen" class="screen active" aria-label="퀴즈">
      <div class="quiz-layout">
        <article class="archive-card question-card">
          <div class="question-kicker">
            <span id="questionNumber">문항 1</span>
            <button id="explanationButton" class="ghost-button" type="button">해설 보기</button>
          </div>
          <p id="questionText" class="question-text">문항을 불러오는 중입니다.</p>
          <div id="choices" class="choices"></div>
          <div id="explanation" class="explanation"></div>
        </article>
        <aside class="archive-card navigator" aria-label="문항 이동">
          <p class="navigator-title">문항 목록</p>
          <div id="numberGrid" class="number-grid"></div>
        </aside>
      </div>
    </section>

    <section id="resultScreen" class="screen" aria-label="결과">
      <div class="archive-card result-panel">
        <p class="question-kicker">채점 결과</p>
        <div id="resultScore" class="result-score">0 / 0</div>
        <p id="resultSummary"></p>
        <div class="result-actions">
          <button id="reviewButton" type="button">정답과 해설 보기</button>
          <button id="retryWrongButton" type="button">오답만 다시 풀기</button>
          <button id="restartButton" class="primary-button" type="button">시험 다시 시작</button>
        </div>
      </div>
    </section>
  </main>

  <nav class="footer-nav" aria-label="풀이 이동">
    <div class="footer-inner">
      <button id="previousButton" type="button">이전</button>
      <button id="submitButton" class="primary-button" type="button">마지막 채점</button>
      <button id="nextButton" type="button">다음</button>
    </div>
  </nav>

  <script>
    const STORAGE_KEYS = {{ progress: "{storage_key}" }};
    const choiceLabels = ["①", "②", "③", "④", "⑤"];

    class QuizApp {{
      constructor() {{
        this.originalQuestions = [];
        this.questions = [];
        this.currentIndex = 0;
        this.answers = {{}};
        this.revealedQuestionIds = new Set();
        this.isSubmitted = false;
        this.reviewMode = false;
        this.elements = {{
          title: document.getElementById("appTitle"),
          quizScreen: document.getElementById("quizScreen"),
          resultScreen: document.getElementById("resultScreen"),
          progressBar: document.getElementById("progressBar"),
          progressText: document.getElementById("progressText"),
          questionNumber: document.getElementById("questionNumber"),
          questionText: document.getElementById("questionText"),
          choices: document.getElementById("choices"),
          numberGrid: document.getElementById("numberGrid"),
          explanation: document.getElementById("explanation")
        }};
        this.bindEvents();
      }}

      bindEvents() {{
        document.getElementById("previousButton").addEventListener("click", () => this.previous());
        document.getElementById("nextButton").addEventListener("click", () => this.next());
        document.getElementById("submitButton").addEventListener("click", () => this.submit());
        document.getElementById("explanationButton").addEventListener("click", () => this.showExplanation());
        document.getElementById("restartButton").addEventListener("click", () => this.restart());
        document.getElementById("retryWrongButton").addEventListener("click", () => this.retryWrongAnswers());
        document.getElementById("reviewButton").addEventListener("click", () => this.reviewAnswers());
      }}

      async loadQuestions() {{
        const response = await fetch("{json_file}", {{ cache: "no-store" }});
        if (!response.ok) throw new Error("{json_file}을 불러오지 못했습니다.");
        const data = await response.json();
        this.elements.title.textContent = data.meta?.title || "{esc_title}";
        this.originalQuestions = data.questions.map(q => structuredClone(q));
        this.loadProgress();
        this.renderQuestion();
      }}

      shuffleQuestions() {{
        this.questions = this.originalQuestions.map(q => structuredClone(q));
        for (let i = this.questions.length - 1; i > 0; i--) {{
          const j = Math.floor(Math.random() * (i + 1));
          [this.questions[i], this.questions[j]] = [this.questions[j], this.questions[i]];
        }}
      }}

      renderQuestion() {{
        if (!this.questions.length) return;
        const q = this.questions[this.currentIndex];
        const answeredCount = Object.keys(this.answers).length;
        const isRevealed = this.reviewMode || this.isSubmitted || this.revealedQuestionIds.has(q.id);
        this.elements.progressBar.style.width = `${{(answeredCount / this.questions.length) * 100}}%`;
        this.elements.progressText.textContent = `${{answeredCount}} / ${{this.questions.length}}`;
        this.elements.questionNumber.textContent = `문항 ${{this.currentIndex + 1}} / ${{this.questions.length}}`;
        this.elements.questionText.textContent = q.question;
        this.elements.choices.innerHTML = "";
        q.choices.forEach((choice, index) => {{
          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "choice";
          btn.setAttribute("aria-label", `${{choiceLabels[index]}} ${{choice}}`);
          btn.innerHTML = `<span class="mark">${{choiceLabels[index]}}</span><span>${{this.escapeHTML(choice)}}</span>`;
          if (this.answers[q.id] === index) btn.classList.add("selected");
          if (isRevealed) {{
            if (index === q.answer) btn.classList.add("correct");
            if (this.answers[q.id] === index && index !== q.answer) btn.classList.add("wrong");
          }}
          btn.addEventListener("click", () => this.selectChoice(index));
          btn.addEventListener("keydown", e => {{
            if (e.key === "Enter" || e.key === " ") {{ e.preventDefault(); this.selectChoice(index); }}
          }});
          this.elements.choices.appendChild(btn);
        }});
        this.elements.explanation.textContent = q.explanation;
        this.elements.explanation.classList.toggle("visible", isRevealed);
        this.renderNumberGrid();
        this.saveProgress();
      }}

      selectChoice(choiceIndex) {{
        if (this.isSubmitted && !this.reviewMode) return;
        const q = this.questions[this.currentIndex];
        if (this.revealedQuestionIds.has(q.id) && !this.reviewMode) return;
        this.answers[q.id] = choiceIndex;
        this.revealedQuestionIds.add(q.id);
        this.renderQuestion();
      }}

      next() {{
        if (this.currentIndex < this.questions.length - 1) {{
          this.currentIndex++;
          this.renderQuestion();
          window.scrollTo({{ top: 0, behavior: "smooth" }});
        }}
      }}

      previous() {{
        if (this.currentIndex > 0) {{
          this.currentIndex--;
          this.renderQuestion();
          window.scrollTo({{ top: 0, behavior: "smooth" }});
        }}
      }}

      jumpTo(index) {{
        this.currentIndex = Math.max(0, Math.min(index, this.questions.length - 1));
        this.renderQuestion();
      }}

      submit() {{
        this.isSubmitted = true;
        const score = this.questions.reduce((t, q) => t + (this.answers[q.id] === q.answer ? 1 : 0), 0);
        document.getElementById("resultScore").textContent = `${{score}} / ${{this.questions.length}}`;
        document.getElementById("resultSummary").textContent = `정답 ${{score}}문항, 오답 ${{this.questions.length - score}}문항입니다.`;
        this.elements.quizScreen.classList.remove("active");
        this.elements.resultScreen.classList.add("active");
        this.saveProgress();
      }}

      showExplanation() {{ this.elements.explanation.classList.toggle("visible"); }}

      retryWrongAnswers() {{
        const wrong = this.questions.filter(q => this.answers[q.id] !== q.answer);
        if (!wrong.length) {{ alert("다시 풀 오답이 없습니다."); return; }}
        this.questions = wrong.map(q => structuredClone(q));
        this.answers = {{}};
        this.revealedQuestionIds = new Set();
        this.currentIndex = 0;
        this.isSubmitted = false;
        this.reviewMode = false;
        this.elements.resultScreen.classList.remove("active");
        this.elements.quizScreen.classList.add("active");
        this.renderQuestion();
      }}

      reviewAnswers() {{
        this.reviewMode = true;
        this.elements.resultScreen.classList.remove("active");
        this.elements.quizScreen.classList.add("active");
        this.currentIndex = 0;
        this.renderQuestion();
      }}

      restart() {{
        localStorage.removeItem(STORAGE_KEYS.progress);
        this.answers = {{}};
        this.revealedQuestionIds = new Set();
        this.currentIndex = 0;
        this.isSubmitted = false;
        this.reviewMode = false;
        this.shuffleQuestions();
        this.elements.resultScreen.classList.remove("active");
        this.elements.quizScreen.classList.add("active");
        this.renderQuestion();
      }}

      saveProgress() {{
        if (!this.questions.length) return;
        localStorage.setItem(STORAGE_KEYS.progress, JSON.stringify({{
          questionIds: this.questions.map(q => q.id),
          currentIndex: this.currentIndex,
          answers: this.answers,
          revealedQuestionIds: [...this.revealedQuestionIds],
          isSubmitted: this.isSubmitted,
          reviewMode: this.reviewMode
        }}));
      }}

      loadProgress() {{
        const saved = JSON.parse(localStorage.getItem(STORAGE_KEYS.progress) || "null");
        if (!saved?.questionIds?.length) {{ this.shuffleQuestions(); return; }}
        const map = new Map(this.originalQuestions.map(q => [q.id, q]));
        this.questions = saved.questionIds.map(id => map.get(id)).filter(Boolean).map(q => structuredClone(q));
        if (this.questions.length !== this.originalQuestions.length) {{ this.shuffleQuestions(); return; }}
        this.currentIndex = Math.min(saved.currentIndex || 0, this.questions.length - 1);
        this.answers = saved.answers || {{}};
        this.revealedQuestionIds = new Set(saved.revealedQuestionIds || []);
        this.isSubmitted = Boolean(saved.isSubmitted);
        this.reviewMode = Boolean(saved.reviewMode);
      }}

      renderNumberGrid() {{
        this.elements.numberGrid.innerHTML = "";
        this.questions.forEach((q, i) => {{
          const btn = document.createElement("button");
          btn.type = "button";
          btn.textContent = i + 1;
          btn.setAttribute("aria-label", `${{i + 1}}번 문항으로 이동`);
          if (i === this.currentIndex) btn.classList.add("current");
          if (this.answers[q.id] !== undefined) btn.classList.add("answered");
          btn.addEventListener("click", () => this.jumpTo(i));
          this.elements.numberGrid.appendChild(btn);
        }});
      }}

      escapeHTML(v) {{
        return String(v).replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]));
      }}
    }}

    document.addEventListener("DOMContentLoaded", async () => {{
      const app = new QuizApp();
      window.quizApp = app;
      try {{
        await app.loadQuestions();
      }} catch (e) {{
        document.getElementById("questionText").textContent = e.message + " 서버에서 올바르게 실행되고 있는지 확인하세요.";
      }}
    }});
  </script>
</body>
</html>"""


def get_quiz_list():
    quizzes = []
    for html_file in sorted(QUIZ_DIR.glob('*.html')):
        name = html_file.stem
        json_file = QUIZ_DIR / (name + '.json')
        info = {'name': name, 'title': name, 'count': 0, 'theme': 'other', 'quiz_type': 'quiz'}
        if json_file.exists():
            try:
                with open(json_file, encoding='utf-8') as f:
                    data = json.load(f)
                if 'meta' in data and 'questions' in data:
                    info['title'] = data.get('meta', {}).get('title', name)
                    info['count'] = len(data.get('questions', []))
                elif 'events' in data:
                    info['title'] = data.get('title', name)
                    info['count'] = len(data.get('events', []))
                    info['quiz_type'] = 'timeline'
            except Exception:
                pass
            for prefix in ('history', 'social', 'science', 'math', 'english', 'korean',
                           'nihongo', 'zhongwen', 'deutsch', 'francais', 'espanol', 'computer'):
                if name.startswith(prefix):
                    info['theme'] = prefix
                    break
        else:
            info['theme'] = 'unofficial'
        quizzes.append(info)
    def _sort_key(q):
        if q['theme'] == 'unofficial':
            return (2, q['name'])
        if q['theme'] == 'other':
            return (1, q['name'])
        return (0, q['name'])
    quizzes.sort(key=_sort_key)
    return quizzes


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
@app.route('/quiz')
def quiz_list():
    quizzes = get_quiz_list()
    return render_template('index.html', quizzes=quizzes, themes=THEMES)


@app.route('/quiz/<name>')
def serve_quiz(name):
    if not re.match(r'^[a-zA-Z0-9]+$', name):
        abort(404)
    html_file = QUIZ_DIR / (name + '.html')
    if not html_file.exists():
        abort(404)
    content = html_file.read_text(encoding='utf-8')
    return Response(content, content_type='text/html; charset=utf-8')


@app.route('/quiz/<name>.json')
def serve_quiz_json(name):
    if not re.match(r'^[a-zA-Z0-9]+$', name):
        abort(404)
    return send_from_directory(str(QUIZ_DIR), name + '.json')


@app.route('/create')
@require_login
def create():
    return render_template('create.html', themes=THEMES,
                           memory_files=MEMORY_FILES, user=session.get('user'))


@app.route('/api/create', methods=['POST'])
@require_login
def api_create():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': '요청 데이터가 없습니다'}), 400

    raw_name = data.get('name', '').strip()
    title = data.get('title', '').strip()
    theme_key = data.get('theme', 'science')
    questions = data.get('questions', [])

    if not raw_name:
        return jsonify({'error': '파일 이름을 입력하세요'}), 400
    if not title:
        return jsonify({'error': '퀴즈 제목을 입력하세요'}), 400
    if theme_key not in THEMES:
        return jsonify({'error': '올바른 테마를 선택하세요'}), 400
    if not questions:
        return jsonify({'error': '문항을 최소 1개 이상 입력하세요'}), 400

    clean_name = sanitize_name(raw_name)
    if not clean_name:
        return jsonify({'error': '파일 이름은 영문자와 숫자만 사용 가능합니다'}), 400

    filename_base = clean_name if clean_name.endswith('danwon') else clean_name + 'danwon'

    html_path = QUIZ_DIR / (filename_base + '.html')
    json_path = QUIZ_DIR / (filename_base + '.json')
    if html_path.exists() or json_path.exists():
        return jsonify({'error': f'"{filename_base}" 이름의 퀴즈가 이미 존재합니다'}), 409

    validated = []
    for i, q in enumerate(questions, 1):
        qtext = str(q.get('question', '')).strip()
        choices = q.get('choices', [])
        answer = q.get('answer')
        expl = str(q.get('explanation', '')).strip()

        if not qtext:
            return jsonify({'error': f'{i}번 문항 질문이 비어있습니다'}), 400
        if not isinstance(choices, list) or len(choices) != 5:
            return jsonify({'error': f'{i}번 문항 선지가 5개여야 합니다'}), 400
        if not all(str(c).strip() for c in choices):
            return jsonify({'error': f'{i}번 문항 선지가 비어있습니다'}), 400
        if not isinstance(answer, int) or answer not in range(5):
            return jsonify({'error': f'{i}번 문항 정답 선택이 잘못되었습니다 (0~4)'}), 400

        validated.append({
            'id': i,
            'question': qtext,
            'choices': [str(c).strip() for c in choices],
            'answer': answer,
            'explanation': expl
        })

    quiz_json = {'meta': {'title': title, 'version': '1.0'}, 'questions': validated}
    quiz_html = generate_quiz_html(filename_base, title, theme_key)

    json_path.write_text(json.dumps(quiz_json, ensure_ascii=False, indent=2), encoding='utf-8')
    html_path.write_text(quiz_html, encoding='utf-8')

    return jsonify({'success': True, 'name': filename_base,
                    'url': url_for('serve_quiz', name=filename_base)})


@app.route('/api/upload', methods=['POST'])
@require_login
def api_upload():
    html_file = request.files.get('html_file')
    json_file_obj = request.files.get('json_file')

    if not html_file:
        return jsonify({'error': 'HTML 파일이 필요합니다'}), 400

    html_name = html_file.filename or ''
    if not html_name.endswith('.html'):
        return jsonify({'error': 'HTML 파일(.html)을 선택하세요'}), 400

    html_base = html_name[:-5]
    safe = sanitize_name(html_base)
    if not safe or safe != html_base:
        return jsonify({'error': '파일 이름은 영문자와 숫자만 허용됩니다'}), 400

    html_path = QUIZ_DIR / (safe + '.html')
    json_path = QUIZ_DIR / (safe + '.json')
    if html_path.exists() or json_path.exists():
        return jsonify({'error': f'"{safe}" 이름의 파일이 이미 존재합니다'}), 409

    # JSON optional — if provided, validate and save; otherwise unofficial mode
    json_data = None
    if json_file_obj and json_file_obj.filename:
        json_name = json_file_obj.filename or ''
        if not json_name.endswith('.json'):
            return jsonify({'error': 'JSON 파일(.json)을 선택하세요'}), 400
        json_base = json_name[:-5]
        if json_base != html_base:
            return jsonify({'error': 'HTML과 JSON 파일 이름(확장자 제외)이 일치해야 합니다'}), 400
        try:
            json_data = json.loads(json_file_obj.read().decode('utf-8'))
        except Exception:
            return jsonify({'error': 'JSON 파일을 읽을 수 없습니다'}), 400
        is_quiz = 'meta' in json_data and 'questions' in json_data
        is_timeline = 'title' in json_data and 'events' in json_data
        if not is_quiz and not is_timeline:
            return jsonify({'error': 'JSON에 (meta+questions) 또는 (title+events) 필드가 필요합니다'}), 400
        if is_quiz and (not isinstance(json_data['questions'], list) or len(json_data['questions']) == 0):
            return jsonify({'error': '문항이 최소 1개 필요합니다'}), 400
        if is_timeline and (not isinstance(json_data['events'], list) or len(json_data['events']) == 0):
            return jsonify({'error': '연표 사건이 최소 1개 필요합니다'}), 400

    html_file.seek(0)
    html_path.write_bytes(html_file.read())
    if json_data is not None:
        json_path.write_text(json.dumps(json_data, ensure_ascii=False, indent=2), encoding='utf-8')

    return jsonify({'success': True, 'name': safe,
                    'url': url_for('serve_quiz', name=safe)})


@app.route('/auth/login')
def auth_login():
    if not os.environ.get('GOOGLE_CLIENT_ID'):
        return render_template('error.html',
                               message='Google OAuth가 설정되지 않았습니다. 관리자에게 문의하세요.')
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth/callback')
def auth_callback():
    try:
        token = google.authorize_access_token()
    except Exception:
        return render_template('error.html', message='구글 로그인에 실패했습니다. 다시 시도해 주세요.')

    user_info = token.get('userinfo', {})
    email = user_info.get('email', '')

    if not email.endswith(f'@{ALLOWED_DOMAIN}'):
        return render_template('error.html',
                               message=f'외대부고 구글 계정(@{ALLOWED_DOMAIN})으로만 로그인할 수 있습니다.',
                               show_back=True)

    session['user'] = {
        'email': email,
        'name': user_info.get('name', email),
        'picture': user_info.get('picture', ''),
    }

    next_url = session.pop('next', None)
    return redirect(next_url or url_for('create'))


@app.route('/auth/logout')
def auth_logout():
    session.pop('user', None)
    return redirect(url_for('quiz_list'))


@app.route('/download/memory/<filename>')
def download_memory(filename):
    allowed = {f for f, _ in MEMORY_FILES}
    if filename not in allowed:
        abort(404)
    return send_from_directory(str(MEMORY_DIR), filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
