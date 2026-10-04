const state = {
  questions: [],
  current: 0,
  selected: new Set(),
  score: 0,
  answered: false,
  mode: 'single'
};

const els = {
  quiz: document.querySelector('#quiz'),
  result: document.querySelector('#result'),
  questionArea: document.querySelector('#questionArea'),
  quizPart: document.querySelector('#quizPart'),
  quizTitle: document.querySelector('#quizTitle'),
  progressText: document.querySelector('#progressText'),
  scoreText: document.querySelector('#scoreText'),
  progressBar: document.querySelector('#progressBar'),
  prev: document.querySelector('#prevQuestion'),
  next: document.querySelector('#nextQuestion')
};

const shuffle = (items) => {
  const copy = [...items];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
};

async function loadQuestions() {
  const response = await fetch('./data/questions.json');
  if (!response.ok) throw new Error('Không thể tải ngân hàng câu hỏi.');
  return response.json();
}

function startQuiz(part = null, count = 5) {
  const pool = state.questions.filter((q) => part === null || q.part === part);
  state.questions = shuffle(pool).slice(0, Math.min(count, pool.length)).map((q) => ({
    ...q,
    variants: [...q.variants],
    answers: shuffle(q.answers)
  }));
  state.current = 0;
  state.score = 0;
  state.selected = new Set();
  state.answered = false;
  els.result.classList.add('hidden');
  els.quiz.classList.remove('hidden');
  els.quiz.scrollIntoView({ behavior: 'smooth', block: 'start' });
  renderQuestion();
}

function renderQuestion() {
  const q = state.questions[state.current];
  if (!q) return;
  state.selected = new Set();
  state.answered = false;
  const variant = q.variants[Math.floor(Math.random() * q.variants.length)];
  const correctCount = q.answers.filter((a) => a.correct).length;
  state.mode = correctCount > 1 ? 'multiple' : 'single';

  els.quizPart.textContent = `Bài ${q.part}`;
  els.quizTitle.textContent = q.topic;
  els.progressText.textContent = `Câu ${state.current + 1} / ${state.questions.length}`;
  els.scoreText.textContent = `Đúng ${state.score}`;
  els.progressBar.style.width = `${((state.current + 1) / state.questions.length) * 100}%`;
  els.prev.disabled = state.current === 0;
  els.next.textContent = state.current === state.questions.length - 1 ? 'Nộp bài' : 'Trả lời & tiếp →';

  els.questionArea.innerHTML = `
    <p class="question-text">${escapeHtml(variant)}</p>
    <div class="answers">
      ${q.answers.map((a, index) => `
        <button class="answer" data-answer-id="${escapeHtml(a.id)}">
          <span class="answer-key">${String.fromCharCode(65 + index)}.</span>
          <span>${escapeHtml(a.text)}</span>
        </button>`).join('')}
    </div>
    <div id="explanation" class="explanation hidden"></div>
  `;

  els.questionArea.querySelectorAll('.answer').forEach((button) => {
    button.addEventListener('click', () => toggleAnswer(button.dataset.answerId));
  });
}

function toggleAnswer(id) {
  if (state.answered) return;
  if (state.mode === 'single') state.selected = new Set([id]);
  else state.selected.has(id) ? state.selected.delete(id) : state.selected.add(id);
  els.questionArea.querySelectorAll('.answer').forEach((button) => {
    button.classList.toggle('selected', state.selected.has(button.dataset.answerId));
  });
}

function submitCurrent() {
  if (state.answered) return true;
  if (!state.selected.size) return false;
  const q = state.questions[state.current];
  const correct = new Set(q.answers.filter((a) => a.correct).map((a) => a.id));
  const isCorrect = correct.size === state.selected.size && [...correct].every((id) => state.selected.has(id));
  if (isCorrect) state.score++;
  state.answered = true;

  els.questionArea.querySelectorAll('.answer').forEach((button) => {
    const answer = q.answers.find((a) => a.id === button.dataset.answerId);
    if (answer.correct) button.classList.add('selected');
  });
  const explanation = document.querySelector('#explanation');
  explanation.classList.remove('hidden');
  explanation.innerHTML = `<strong>${isCorrect ? '✓ Đúng' : '✗ Chưa chính xác'}</strong><br>${q.answers.filter(a => a.correct).map(a => escapeHtml(a.explanation)).join('<br>')}`;
  els.scoreText.textContent = `Đúng ${state.score}`;
  return true;
}

function next() {
  if (!submitCurrent()) return;
  if (state.current < state.questions.length - 1) {
    state.current++;
    renderQuestion();
  } else {
    showResult();
  }
}

function showResult() {
  const total = state.questions.length;
  const percent = total ? Math.round((state.score / total) * 100) : 0;
  els.quiz.classList.add('hidden');
  els.result.classList.remove('hidden');
  els.result.innerHTML = `
    <p class="eyebrow">Hoàn thành</p>
    <h2>Kết quả luyện tập</h2>
    <div class="result-score">${state.score}/${total}</div>
    <p>${percent}% câu trả lời đúng.</p>
    <button id="retry" class="primary-button">Làm lại</button>
  `;
  document.querySelector('#retry').addEventListener('click', () => startQuiz(null, total));
  els.result.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
}

document.querySelectorAll('.exam-card').forEach((card) => {
  card.addEventListener('click', () => startQuiz(Number(card.dataset.part), 5));
});
document.querySelector('#practiceAll').addEventListener('click', () => startQuiz(null, 5));

document.querySelector('#exitQuiz').addEventListener('click', () => els.quiz.classList.add('hidden'));
els.prev.addEventListener('click', () => {
  if (state.current > 0) { state.current--; renderQuestion(); }
});
els.next.addEventListener('click', next);

loadQuestions()
  .then((questions) => { state.questions = questions; })
  .catch((error) => {
    console.error(error);
    document.querySelector('main').insertAdjacentHTML('beforeend', `<p class="result-panel">${escapeHtml(error.message)}</p>`);
  });
