'use strict';

const CHOICE_LABELS = ['①', '②', '③', '④', '⑤'];
let questionCount = 0;

// ── Tab switching ─────────────────────────────────────────────────
document.querySelectorAll('.create-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.create-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
  });
});

// ── Subject / filename preview ────────────────────────────────────
function onSubjectChange() {
  const val = document.getElementById('subjectSelect').value;
  const customGroup = document.getElementById('customSubjectGroup');
  customGroup.style.display = val === 'custom' ? 'block' : 'none';
  onNameChange();
}

function onNameChange() {
  const subject = getSubjectPrefix();
  const unit = document.getElementById('unitCode').value.replace(/[^0-9]/g, '');
  const base = subject + unit + 'danwon';
  document.getElementById('filenamePreview').innerHTML =
    `<span class="filename-html">${escHTML(base)}.html</span>` +
    `<span class="filename-sep">+</span>` +
    `<span class="filename-json">${escHTML(base)}.json</span>`;
}

function getSubjectPrefix() {
  const sel = document.getElementById('subjectSelect').value;
  if (sel === 'custom') {
    return document.getElementById('customSubject').value.replace(/[^a-zA-Z]/g, '').toLowerCase();
  }
  return sel;
}

// ── Questions ─────────────────────────────────────────────────────
function addQuestion() {
  questionCount++;
  const idx = questionCount;
  const list = document.getElementById('questionList');

  const item = document.createElement('div');
  item.className = 'q-item';
  item.dataset.idx = idx;

  item.innerHTML = `
    <div class="q-item-header">
      <span class="q-item-num">문항 ${idx}</span>
      <button type="button" class="q-item-del" onclick="removeQuestion(this)">삭제</button>
    </div>
    <div class="q-item-body">
      <div>
        <div class="q-label-sm">문제</div>
        <textarea class="q-textarea" name="question" placeholder="사료나 지문 포함하여 문제를 입력하세요" rows="3"></textarea>
      </div>
      <div>
        <div class="q-label-sm">선지 &nbsp;<span style="color:var(--site-muted);font-weight:400;font-size:.78rem">— 정답 선지 앞 라디오 버튼 선택</span></div>
        <div class="choices-grid">
          ${CHOICE_LABELS.map((lbl, i) => `
          <div class="choice-row">
            <span class="choice-label-badge">${lbl}</span>
            <input type="radio" class="choice-radio" name="answer_${idx}" value="${i}" ${i === 0 ? 'checked' : ''}>
            <input type="text" class="choice-input" name="choice" placeholder="선지 ${i + 1}" autocomplete="off">
            <span class="choice-correct-hint" style="${i === 0 ? '' : 'visibility:hidden'}">← 정답</span>
          </div>`).join('')}
        </div>
      </div>
      <div>
        <div class="q-label-sm">해설 <span style="color:var(--site-muted);font-weight:400;font-size:.78rem">(마크다운 사용 금지, 선지 번호는 ①②③④⑤ 기호 사용)</span></div>
        <textarea class="q-textarea" name="explanation" placeholder="정답 근거 및 오답 선지 분석을 작성하세요" rows="3"></textarea>
      </div>
    </div>`;

  // Update "correct answer" hint on radio change
  item.querySelectorAll('.choice-radio').forEach(radio => {
    radio.addEventListener('change', () => {
      item.querySelectorAll('.choice-correct-hint').forEach(h => h.style.visibility = 'hidden');
      radio.closest('.choice-row').querySelector('.choice-correct-hint').style.visibility = 'visible';
    });
  });

  list.appendChild(item);
  updateQuestionCount();
  item.querySelector('.q-textarea').focus();
}

function removeQuestion(btn) {
  const item = btn.closest('.q-item');
  item.remove();
  renumberQuestions();
  updateQuestionCount();
}

function renumberQuestions() {
  document.querySelectorAll('.q-item').forEach((item, i) => {
    item.querySelector('.q-item-num').textContent = `문항 ${i + 1}`;
  });
}

function updateQuestionCount() {
  const count = document.querySelectorAll('.q-item').length;
  document.getElementById('qCount').textContent = count + '문항';
}

// ── Form submission ───────────────────────────────────────────────
document.getElementById('createForm').addEventListener('submit', async e => {
  e.preventDefault();
  const btn = document.getElementById('submitBtn');
  const errEl = document.getElementById('submitError');
  errEl.classList.remove('visible');

  const subjectPrefix = getSubjectPrefix();
  const unit = document.getElementById('unitCode').value.replace(/[^0-9]/g, '');
  if (!subjectPrefix) { showError(errEl, '과목 이름을 입력하세요'); return; }
  if (!unit) { showError(errEl, '단원 코드를 입력하세요 (숫자)'); return; }

  const name = subjectPrefix + unit;
  const title = document.getElementById('quizTitle').value.trim();
  if (!title) { showError(errEl, '퀴즈 제목을 입력하세요'); return; }

  const theme = document.querySelector('input[name="theme"]:checked')?.value || 'science';

  const items = document.querySelectorAll('.q-item');
  if (!items.length) { showError(errEl, '문항을 최소 1개 추가하세요'); return; }

  const questions = [];
  for (const [i, item] of [...items].entries()) {
    const qNum = i + 1;
    const question = item.querySelector('textarea[name="question"]').value.trim();
    const choiceInputs = item.querySelectorAll('input[name="choice"]');
    const choices = [...choiceInputs].map(c => c.value.trim());
    const answerRadio = item.querySelector(`input[name="answer_${item.dataset.idx}"]:checked`);
    const answer = answerRadio ? parseInt(answerRadio.value) : 0;
    const explanation = item.querySelector('textarea[name="explanation"]').value.trim();

    if (!question) { showError(errEl, `${qNum}번 문항 질문을 입력하세요`); return; }
    if (choices.some(c => !c)) { showError(errEl, `${qNum}번 문항의 모든 선지를 입력하세요`); return; }

    questions.push({ question, choices, answer, explanation });
  }

  btn.textContent = '생성 중...';
  btn.disabled = true;

  try {
    const res = await fetch('/api/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, title, theme, questions })
    });
    const data = await res.json();
    if (!res.ok) { showError(errEl, data.error || '오류가 발생했습니다'); return; }
    showSuccess(data.url, data.name);
  } catch {
    showError(errEl, '서버 연결 오류가 발생했습니다');
  } finally {
    btn.textContent = '퀴즈 생성';
    btn.disabled = false;
  }
});

// ── Upload ────────────────────────────────────────────────────────
function onUploadChange() {
  const htmlInput = document.getElementById('uploadHtml');
  const jsonInput = document.getElementById('uploadJson');
  document.getElementById('htmlHint').textContent =
    htmlInput.files[0] ? htmlInput.files[0].name : '클릭하여 .html 파일 선택';
  document.getElementById('jsonHint').textContent =
    jsonInput.files[0] ? jsonInput.files[0].name : '클릭하여 .json 파일 선택';
  if (htmlInput.files[0]) document.getElementById('htmlHint').classList.add('has-file');
  else document.getElementById('htmlHint').classList.remove('has-file');
  if (jsonInput.files[0]) document.getElementById('jsonHint').classList.add('has-file');
  else document.getElementById('jsonHint').classList.remove('has-file');
}

document.getElementById('uploadForm').addEventListener('submit', async e => {
  e.preventDefault();
  const btn = document.getElementById('uploadBtn');
  const errEl = document.getElementById('uploadError');
  errEl.classList.remove('visible');

  const htmlFile = document.getElementById('uploadHtml').files[0];
  const jsonFile = document.getElementById('uploadJson').files[0];

  if (!htmlFile || !jsonFile) { showError(errEl, 'HTML과 JSON 파일을 모두 선택하세요'); return; }

  const fd = new FormData();
  fd.append('html_file', htmlFile);
  fd.append('json_file', jsonFile);

  btn.textContent = '업로드 중...';
  btn.disabled = true;

  try {
    const res = await fetch('/api/upload', { method: 'POST', body: fd });
    const data = await res.json();
    if (!res.ok) { showError(errEl, data.error || '오류가 발생했습니다'); return; }
    showSuccess(data.url, data.name);
  } catch {
    showError(errEl, '서버 연결 오류가 발생했습니다');
  } finally {
    btn.textContent = '업로드';
    btn.disabled = false;
  }
});

// ── AI Prompt copy ────────────────────────────────────────────────
function copyPrompt() {
  const text = document.getElementById('aiPromptText').innerText;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('.copy-prompt-btn');
    btn.textContent = '복사됨!';
    setTimeout(() => { btn.textContent = '복사'; }, 2000);
  });
}

// ── Helpers ───────────────────────────────────────────────────────
function showError(el, msg) {
  el.textContent = msg;
  el.classList.add('visible');
}

function showSuccess(quizUrl, name) {
  document.getElementById('modalMsg').textContent = `"${name}" 퀴즈가 생성되었습니다.`;
  document.getElementById('modalQuizLink').href = quizUrl;
  document.getElementById('successModal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('successModal').style.display = 'none';
}

function escHTML(str) {
  return String(str).replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// Init: update filename preview on load
onNameChange();
