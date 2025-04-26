// app.js

let words = [];
let currentCandidates = [];

const headEl    = document.getElementById('head');
const tailEl    = document.getElementById('tail');
const answerEl  = document.getElementById('answer');
const resultEl  = document.getElementById('result');
const scoreEl   = document.getElementById('score');
const submitBtn = document.getElementById('submit');

// JSON 辞書読み込み
fetch('words.json')
  .then(res => res.json())
  .then(data => {
    words = data;
    startGame();
  })
  .catch(err => {
    console.error('辞書の読み込み失敗:', err);
    resultEl.textContent = '辞書読み込みエラー';
  });

// 新しいゲーム／次の問題開始
function startGame() {
  // フィードバッククリア＆入力初期化
  resultEl.textContent = '';
  scoreEl.textContent  = '';
  resultEl.className   = '';
  scoreEl.className    = '';
  answerEl.value       = '';
  answerEl.disabled    = false;
  submitBtn.disabled   = false;

  // 頭文字・語尾候補抽出
  const heads = [...new Set(words.map(w => w[0]))];
  const tails = [...new Set(words.map(w => w.slice(-1)))];

  // 有効な組み合わせが得られるまでループ
  do {
    var head = heads[Math.floor(Math.random() * heads.length)];
    var tail = tails[Math.floor(Math.random() * tails.length)];
    currentCandidates = words.filter(w => w[0] === head && w.slice(-1) === tail);
  } while (currentCandidates.length === 0);

  headEl.textContent = head;
  tailEl.textContent = tail;
  answerEl.focus();
}

// 配列をシャッフルするヘルパー
function shuffle(array) {
  return array
    .map(v => ({ v, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(({ v }) => v);
}

// フィードバック表示
function showFeedback(isCorrect, pts) {
  answerEl.disabled  = true;
  submitBtn.disabled = true;

  if (isCorrect) {
    resultEl.textContent = '正解！🎉';
    resultEl.classList.add('text-green-500', 'animate-pulse-slow');
    scoreEl.textContent  = `スコア：${pts} 点`;
  } else {
    resultEl.textContent = '不正解…😢';
    resultEl.classList.add('text-red-500', 'animate-shake');
  }

  setTimeout(startGame, 1500);
}

// 回答ボタン処理
submitBtn.addEventListener('click', () => {
  const ans = answerEl.value.trim();

  // 空欄 or 間違い → 候補の例を提示し、次の問題へ
  if (!ans || !currentCandidates.includes(ans)) {
    const hints = shuffle(currentCandidates).slice(0, 3);
    resultEl.textContent = '候補の例: ' + hints.join('、');
    scoreEl.textContent  = '';
    // 1.5秒後に次の問題へ自動遷移
    setTimeout(startGame, 1500);
    return;
  }

  // 正解時
  const pts = ans.length - 2;
  showFeedback(true, pts);
});

// Enter キーで回答
answerEl.addEventListener('keypress', e => {
  if (e.key === 'Enter') submitBtn.click();
});
