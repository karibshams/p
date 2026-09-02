/* ═══════════════════════════════════════════════
   KARIB SHAMS PORTFOLIO v3 — main.js
   Free AI · 30-Question Quiz · No API · No Cost
═══════════════════════════════════════════════ */

// ── CURSOR ────────────────────────────────────
const cDot  = document.getElementById('cDot');
const cRing = document.getElementById('cRing');
let mx=0, my=0, rx=0, ry=0;
document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cDot.style.left = mx+'px'; cDot.style.top = my+'px';
});
(function animCursor() {
  rx += (mx-rx)*.1; ry += (my-ry)*.1;
  cRing.style.left = rx+'px'; cRing.style.top = ry+'px';
  requestAnimationFrame(animCursor);
})();
document.querySelectorAll('a,button,.proj-card,.sk-tag,.pub-card').forEach(el => {
  el.addEventListener('mouseenter', () => { cRing.style.width='46px'; cRing.style.height='46px'; cRing.style.background='rgba(0,255,194,.07)'; });
  el.addEventListener('mouseleave', () => { cRing.style.width='30px'; cRing.style.height='30px'; cRing.style.background='transparent'; });
});

// ── NEURAL CANVAS ─────────────────────────────
const canvas = document.getElementById('neural-bg');
const ctx    = canvas.getContext('2d');
let W, H;
function resizeCanvas() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const NODES = Array.from({length:80}, () => ({
  x: Math.random()*window.innerWidth, y: Math.random()*window.innerHeight,
  vx:(Math.random()-.5)*.35, vy:(Math.random()-.5)*.35,
  r: Math.random()*1.8+.7, phase: Math.random()*Math.PI*2,
}));

(function drawLoop() {
  ctx.clearRect(0, 0, W, H);
  NODES.forEach(n => {
    n.x+=n.vx; n.y+=n.vy; n.phase+=.018;
    if(n.x<0||n.x>W) n.vx*=-1;
    if(n.y<0||n.y>H) n.vy*=-1;
  });
  for(let i=0;i<NODES.length;i++) {
    for(let j=i+1;j<NODES.length;j++) {
      const dx=NODES[i].x-NODES[j].x, dy=NODES[i].y-NODES[j].y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<130) {
        ctx.beginPath();
        ctx.moveTo(NODES[i].x, NODES[i].y);
        ctx.lineTo(NODES[j].x, NODES[j].y);
        ctx.strokeStyle=`rgba(0,255,194,${(1-d/130)*.22})`;
        ctx.lineWidth=.5; ctx.stroke();
      }
    }
    const p = Math.abs(Math.sin(NODES[i].phase));
    ctx.beginPath();
    ctx.arc(NODES[i].x, NODES[i].y, NODES[i].r+p*.5, 0, Math.PI*2);
    ctx.fillStyle=`rgba(0,255,194,${.2+p*.3})`; ctx.fill();
  }
  requestAnimationFrame(drawLoop);
})();

// ── TYPING EFFECT ─────────────────────────────
const ROLES = [
  'Data Scientist', 'AI Developer', 'Research Assistant',
  'ML Engineer', 'NLP Specialist', 'Computer Vision Engineer',
  'LLM Systems Builder', 'RAG Architect', 'XAI Researcher',
];
let ti=0, ci=0, deleting=false;
const typedEl = document.getElementById('typedEl');
function typeLoop() {
  const cur = ROLES[ti];
  if (!deleting) {
    typedEl.textContent = cur.slice(0, ++ci);
    if (ci === cur.length) { deleting=true; setTimeout(typeLoop, 2200); return; }
  } else {
    typedEl.textContent = cur.slice(0, --ci);
    if (ci === 0) { deleting=false; ti=(ti+1)%ROLES.length; }
  }
  setTimeout(typeLoop, deleting ? 45 : 85);
}
typeLoop();

// ── COUNTERS ──────────────────────────────────
function runCounters() {
  document.querySelectorAll('.hn[data-count]').forEach(el => {
    const target = +el.dataset.count;
    let cur = 0; const step = target/45;
    const t = setInterval(() => {
      cur += step;
      if (cur >= target) { el.textContent = target+(target>=10?'+':''); clearInterval(t); }
      else el.textContent = Math.floor(cur);
    }, 35);
  });
}

// ── SCROLL REVEAL ─────────────────────────────
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if(e.isIntersecting) { e.target.classList.add('vis'); revealObs.unobserve(e.target); } });
}, { threshold:.1 });
document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

const heroObs = new IntersectionObserver(e => {
  if(e[0].isIntersecting) { runCounters(); heroObs.disconnect(); }
}, { threshold:.4 });
const heroStats = document.querySelector('.hero-stats');
if (heroStats) heroObs.observe(heroStats);

// ── NAVBAR ────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.style.background = window.scrollY > 20 ? 'rgba(26,30,35,.96)' : 'rgba(26,30,35,.88)';
  let cur = '';
  document.querySelectorAll('section[id]').forEach(s => { if(window.scrollY >= s.offsetTop-90) cur = s.id; });
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.toggle('active', a.getAttribute('href')==='#'+cur));
});
document.getElementById('navToggle').addEventListener('click', () => document.getElementById('navLinks').classList.toggle('open'));
document.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => document.getElementById('navLinks').classList.remove('open')));

// ── PROJECT FILTER ────────────────────────────
document.querySelectorAll('.ptab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.ptab').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    document.querySelectorAll('.proj-card').forEach(c => c.classList.toggle('hidden', f!=='all' && c.dataset.type!==f));
  });
});

// ── QUIZ — 30 Questions, Random, No Repeats ───
const ALL_QS = [
  // Machine Learning
  { q:"What does 'overfitting' mean in ML?", opts:["Model performs well on training but poorly on test data","Model performs poorly on all data","Model has too few parameters","Training loss is zero"], a:0, exp:"Overfitting: model memorises training data but fails to generalise to unseen data." },
  { q:"Which metric is most suitable for imbalanced classification?", opts:["Accuracy","Precision","F1-Score","R² Score"], a:2, exp:"F1-Score balances precision and recall, making it better for imbalanced datasets." },
  { q:"What is the 'bias-variance tradeoff' in ML?", opts:["Trading model speed for accuracy","Balancing underfitting (high bias) and overfitting (high variance)","Choosing between supervised and unsupervised","Selecting learning rate vs batch size"], a:1, exp:"High bias = underfitting; high variance = overfitting. The tradeoff is finding the sweet spot." },
  { q:"What does 'gradient descent' do?", opts:["Increases model complexity","Finds the minimum of a loss function iteratively","Selects the best features","Splits data into train/test sets"], a:1, exp:"Gradient descent iteratively adjusts weights in the direction that minimises the loss function." },
  { q:"Which algorithm is an ensemble method?", opts:["Logistic Regression","K-Means","Random Forest","Linear SVM"], a:2, exp:"Random Forest is an ensemble of decision trees using bagging." },
  { q:"What does 'regularisation' prevent in ML?", opts:["Underfitting","Overfitting","Slow training","Poor data quality"], a:1, exp:"Regularisation (L1/L2) adds penalties to large weights, preventing overfitting." },
  // Deep Learning
  { q:"What activation function is most common in hidden layers of deep networks?", opts:["Sigmoid","Tanh","ReLU","Softmax"], a:2, exp:"ReLU (Rectified Linear Unit) is the default choice — simple, fast, avoids vanishing gradients." },
  { q:"What is 'batch normalisation' used for?", opts:["Data augmentation","Normalising inputs of each layer to stabilise training","Reducing dataset size","Setting learning rate"], a:1, exp:"Batch normalisation normalises layer inputs, speeding up training and improving stability." },
  { q:"Which architecture is most suitable for sequential data?", opts:["CNN","LSTM","GAN","Autoencoder"], a:1, exp:"LSTM (Long Short-Term Memory) is designed for sequential and time-series data." },
  { q:"What is a GAN composed of?", opts:["Encoder and Decoder","Generator and Discriminator","CNN and RNN","Transformer and BERT"], a:1, exp:"GANs have a Generator (creates fake data) and a Discriminator (distinguishes real from fake)." },
  { q:"What does 'dropout' do in neural networks?", opts:["Reduces learning rate","Randomly deactivates neurons during training to prevent overfitting","Adds more layers","Normalises inputs"], a:1, exp:"Dropout randomly deactivates a fraction of neurons each training step, acting as regularisation." },
  // Transformers & NLP
  { q:"What is the core innovation of the Transformer architecture?", opts:["Convolutional layers","Recurrent connections","Self-attention mechanism","Max pooling layers"], a:2, exp:"Self-attention lets the model weigh the importance of all positions simultaneously — no recurrence needed." },
  { q:"What does BERT stand for?", opts:["Binary Encoding Representation Transformer","Bidirectional Encoder Representations from Transformers","Basic Evaluation and Ranking Technique","Batch-Enhanced Recurrent Transformer"], a:1, exp:"BERT = Bidirectional Encoder Representations from Transformers, pre-trained with masked language modelling." },
  { q:"What is 'tokenisation' in NLP?", opts:["Converting text to lowercase","Splitting text into tokens (words/subwords)","Removing stop words","Translating between languages"], a:1, exp:"Tokenisation splits raw text into tokens that the model can process — words, subwords, or characters." },
  { q:"What is 'fine-tuning' an LLM?", opts:["Training from scratch on a new dataset","Training a pre-trained model further on task-specific data","Compressing the model size","Reducing model vocabulary"], a:1, exp:"Fine-tuning adapts a pre-trained LLM to a specific task using a smaller, domain-specific dataset." },
  { q:"What is RAG in AI?", opts:["Random Augmented Generation","Retrieval-Augmented Generation","Recursive Attention Gate","Rapid AI Graph"], a:1, exp:"RAG retrieves relevant documents and combines them with an LLM to generate grounded, factual answers." },
  // Computer Vision
  { q:"What does YOLO stand for?", opts:["You Obviously Like Operations","You Only Look Once","Your Output Learns Often","Yet Another Object Locator"], a:1, exp:"YOLO = You Only Look Once — processes the entire image in one forward pass for real-time detection." },
  { q:"What is the purpose of a CNN's pooling layer?", opts:["Adds more features","Reduces spatial dimensions while retaining key information","Increases image resolution","Normalises pixel values"], a:1, exp:"Pooling (Max/Average) reduces spatial size, reducing computation and providing translation invariance." },
  { q:"What is 'semantic segmentation'?", opts:["Detecting object bounding boxes","Assigning a class label to every pixel in an image","Tracking objects across video frames","Classifying entire images into categories"], a:1, exp:"Semantic segmentation classifies every pixel — unlike detection which uses bounding boxes." },
  { q:"Swin Transformer uses which type of attention?", opts:["Global attention","Sparse attention","Shifted Window attention","Cross attention"], a:2, exp:"Swin Transformer uses shifted window attention, giving linear complexity and hierarchical features." },
  // XAI & Advanced
  { q:"What does SHAP stand for?", opts:["Shapely Analysis Protocol","SHapley Additive exPlanations","Statistical Heuristic Analysis Procedure","Structural Hierarchical AI Proxy"], a:1, exp:"SHAP assigns each feature a contribution value based on cooperative game theory (Shapley values)." },
  { q:"What is XGBoost optimised for?", opts:["Image classification","Gradient boosted decision trees on tabular data","Generative image synthesis","Large language model training"], a:1, exp:"XGBoost is an optimised, regularised gradient boosting framework excelling on tabular/structured data." },
  { q:"What is 'transfer learning'?", opts:["Sending a model to another computer","Using knowledge from one task to improve performance on another","Training on multiple GPUs simultaneously","Copying training data between datasets"], a:1, exp:"Transfer learning reuses a model trained on one task (e.g., ImageNet) for a related task, saving time and data." },
  { q:"What is a 'knowledge graph'?", opts:["A performance benchmark chart","A graph database of entities and their relationships","A type of neural network topology","A visual representation of training loss"], a:1, exp:"Knowledge graphs represent real-world entities as nodes and relationships as edges — enabling semantic reasoning." },
  // Data Science
  { q:"What is 'feature engineering'?", opts:["Designing the neural network architecture","Creating or transforming input features to improve model performance","Selecting the right GPU","Writing model evaluation reports"], a:1, exp:"Feature engineering creates new informative features from raw data to help ML models perform better." },
  { q:"What is the purpose of cross-validation?", opts:["Cleaning data","Estimating model performance more reliably using multiple train/test splits","Choosing the right algorithm","Visualising data distributions"], a:1, exp:"Cross-validation (e.g., k-fold) gives a more reliable performance estimate than a single train-test split." },
  { q:"What does 'dimensionality reduction' do?", opts:["Increases data size","Reduces the number of input features while preserving important information","Removes outliers","Normalises data distribution"], a:1, exp:"Techniques like PCA and t-SNE reduce feature dimensions, aiding visualisation and reducing computation." },
  // Semi/Self-supervised
  { q:"What is 'self-supervised learning'?", opts:["Learning with human-provided labels","Learning from synthetic datasets","Generating supervisory signals from the data itself","Training only on test data"], a:2, exp:"Self-supervised learning creates labels from data structure (e.g., predict masked tokens, contrastive pairs)." },
  { q:"In contrastive learning, what are 'positive pairs'?", opts:["Two samples from different classes","Two augmented views of the same sample","Samples with the highest confidence","Random pairs from the dataset"], a:1, exp:"Positive pairs are two different augmentations of the same data point — the model learns they should be similar." },
  // Misc AI
  { q:"What does n8n enable in AI workflows?", opts:["Training neural networks","Visual workflow automation connecting APIs and AI services","Database management","Writing Python scripts"], a:1, exp:"n8n is an open-source workflow automation tool — you can connect LLMs, APIs, and webhooks without heavy coding." },
];

function shuffle(arr) {
  const a = [...arr];
  for(let i=a.length-1; i>0; i--) { const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}

let quizQuestions=[], qi=0, sc=0;

function initQuiz() {
  quizQuestions = shuffle(ALL_QS);
  qi = 0; sc = 0;
  document.getElementById('qscore').textContent = 'Score: 0/'+quizQuestions.length;
  document.getElementById('quiz-body').innerHTML = '<div id="qq" class="quiz-q"></div><div id="qopts" class="quiz-opts"></div><div id="qexp" class="quiz-exp" style="display:none"></div>';
  showQ();
}

function showQ() {
  if (qi >= quizQuestions.length) {
    const pct = Math.round((sc/quizQuestions.length)*100);
    const grade = pct>=90?'🏆 Outstanding!':pct>=70?'⭐ Great job!':pct>=50?'👍 Good effort!':'🤖 Keep learning!';
    document.getElementById('quiz-body').innerHTML = `
      <div class="quiz-result">
        <h3>${grade}</h3>
        <p>Score: ${sc}/${quizQuestions.length} &nbsp;·&nbsp; ${pct}% correct</p>
        <button class="btn-primary" onclick="initQuiz()">🔄 Play Again (New Order)</button>
      </div>`;
    document.getElementById('qscore').textContent = 'Final: '+sc+'/'+quizQuestions.length;
    return;
  }
  const q = quizQuestions[qi];
  document.getElementById('qq').textContent = `Q${qi+1}/${quizQuestions.length}: ${q.q}`;
  const oe = document.getElementById('qopts'); oe.innerHTML = '';
  const expEl = document.getElementById('qexp'); expEl.style.display='none'; expEl.textContent='';
  q.opts.forEach((opt, i) => {
    const b = document.createElement('button');
    b.className = 'q-opt'; b.textContent = opt;
    b.onclick = () => {
      Array.from(oe.children).forEach(x => x.disabled=true);
      if (i===q.a) { b.classList.add('correct'); sc++; }
      else { b.classList.add('wrong'); oe.children[q.a].classList.add('correct'); }
      expEl.textContent = '💡 '+q.exp; expEl.style.display='block';
      document.getElementById('qscore').textContent = 'Score: '+sc+'/'+quizQuestions.length;
      qi++;
      setTimeout(showQ, 1800);
    };
    oe.appendChild(b);
  });
}

// ── AI CHAT (Free Django Backend) ────────────
async function sendChat() {
  const inp = document.getElementById('chatInput');
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = '';
  hideSugg();
  addMsg(msg, 'user');
  const tid = 't'+Date.now(); addTyping(tid);
  try {
    const res = await fetch('/api/chat/', {
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body: JSON.stringify({message: msg}),
    });
    const data = await res.json();
    removeTyping(tid);
    addMsg(data.reply || 'No response.', 'bot');
  } catch {
    removeTyping(tid);
    addMsg('Connection error. Please try again.', 'bot');
  }
}
function sendSug(btn) { document.getElementById('chatInput').value = btn.textContent; sendChat(); }
function hideSugg() { const s=document.getElementById('chatSugg'); if(s) s.style.display='none'; }
function clearChat() {
  document.getElementById('chatMsgs').innerHTML = `
    <div class="cm bot"><span class="bav">🤖</span>
    <div class="bubble">Chat cleared! Ask me anything about Karib's research, projects, team, or any AI/ML concept.</div></div>`;
  const s=document.getElementById('chatSugg'); if(s) s.style.display='flex';
}
function addMsg(text, role) {
  const wrap = document.getElementById('chatMsgs');
  const d = document.createElement('div');
  d.className = 'cm '+role;
  const fmt = esc(text).replace(/\n/g,'<br/>');
  d.innerHTML = role==='bot'
    ? `<span class="bav">🤖</span><div class="bubble">${fmt}</div>`
    : `<div class="bubble">${fmt}</div>`;
  wrap.appendChild(d);
  wrap.scrollTop = wrap.scrollHeight;
}
function addTyping(id) {
  const wrap = document.getElementById('chatMsgs');
  const d = document.createElement('div'); d.className='cm bot'; d.id=id;
  d.innerHTML='<span class="bav">🤖</span><div class="bubble"><span class="typing-dots"><span>●</span><span>●</span><span>●</span></span></div>';
  wrap.appendChild(d); wrap.scrollTop=wrap.scrollHeight;
}
function removeTyping(id) { const el=document.getElementById(id); if(el) el.remove(); }
document.getElementById('chatInput').addEventListener('keydown', e => { if(e.key==='Enter') sendChat(); });

// ── FEEDBACK ──────────────────────────────────
async function submitFeedback(e) {
  e.preventDefault();
  const res = document.getElementById('fb-res');
  try {
    const r = await fetch('/api/feedback/', {
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':csrf()},
      body: JSON.stringify({
        name: document.getElementById('fb-name').value,
        email: document.getElementById('fb-email').value,
        message: document.getElementById('fb-msg').value,
      }),
    });
    const d = await r.json();
    res.style.color='var(--acc)'; res.style.fontFamily='var(--mono)'; res.style.fontSize='.8rem'; res.style.marginTop='.5rem';
    res.textContent = d.msg || 'Submitted!';
    document.getElementById('fbForm').reset();
    setTimeout(()=>res.textContent='', 4000);
  } catch {
    res.textContent = 'Error. Please try again.';
  }
}

// ── FILE UPLOAD ───────────────────────────────
const uz = document.getElementById('uploadZone');
const fi = document.getElementById('fileInput');
const ur = document.getElementById('uploadResult');
uz.addEventListener('dragover', e => { e.preventDefault(); uz.style.borderColor='var(--acc)'; });
uz.addEventListener('dragleave', () => uz.style.borderColor='');
uz.addEventListener('drop', e => { e.preventDefault(); uz.style.borderColor=''; if(e.dataTransfer.files[0]) showUpload(e.dataTransfer.files[0]); });
fi.addEventListener('change', () => { if(fi.files[0]) showUpload(fi.files[0]); });
function showUpload(f) {
  ur.innerHTML = `✅ <strong>${esc(f.name)}</strong> (${(f.size/1024).toFixed(1)} KB) — ready to showcase!`;
  setTimeout(()=>ur.innerHTML='', 5000);
}

// ── UTILS ─────────────────────────────────────
function esc(t) { return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function csrf() { return document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''; }

/* ═══════════════════════════════════════════════
   AI ROBOT GUIDE
═══════════════════════════════════════════════ */

// Section messages robot says as user scrolls
const ROBOT_MSGS = {
  'hero':         "Hi! I'm Karib's AI Robot Guide! 🤖 Welcome to his portfolio — explore and ask me anything!",
  'about':        "📖 Let me tell you about Karib's journey — MSc in Data Science, GTA, Researcher, and Team Leader!",
  'skills':       "⚙️ Karib masters Python, Deep Learning, RAG, NLP, Computer Vision, n8n, and much more!",
  'experience':   "💼 Karib leads a night team at JVai building RAG chatbots and AI automation systems!",
  'projects':     "🚀 These are real AI products Karib built — including live deployed apps at emothrive.net!",
  'publications': "🏆 16 published papers across IEEE, Springer & Nature! Best Paper Award in Washington D.C.!",
  'aichat':       "💬 Ask me anything! I'm Karib's free AI — I know all his research, projects and AI/ML concepts!",
  'feedback':     "📝 Leave your feedback! Karib personally reads every message!",
  'contact':      "📞 Want to collaborate? Reach Karib on WhatsApp or Email — he responds fast!",
};

let robotChatOpen   = false;
let lastRobotSection = '';
let bubbleTimeout;

// Toggle robot chat panel
function toggleRobotChat() {
  robotChatOpen = !robotChatOpen;
  const chat   = document.getElementById('robot-chat');
  const bubble = document.getElementById('robot-bubble');
  if (robotChatOpen) {
    chat.classList.remove('hidden');
    bubble.classList.add('hidden');
    document.getElementById('rcInput').focus();
  } else {
    chat.classList.add('hidden');
    bubble.classList.remove('hidden');
  }
}

// Show speech bubble with message
function showRobotBubble(msg) {
  const bubble = document.getElementById('robot-bubble');
  const text   = document.getElementById('robot-bubble-text');
  if (robotChatOpen) return;
  clearTimeout(bubbleTimeout);
  text.textContent = msg;
  bubble.classList.remove('hidden');
  bubbleTimeout = setTimeout(() => {
    bubble.classList.add('hidden');
  }, 5000);
}

// Detect which section is in view → show robot message
function checkRobotSection() {
  if (robotChatOpen) return;
  const sections = document.querySelectorAll('section[id]');
  let current = '';
  sections.forEach(s => {
    const rect = s.getBoundingClientRect();
    if (rect.top <= window.innerHeight * .5 && rect.bottom >= window.innerHeight * .3) {
      current = s.id;
    }
  });
  if (current && current !== lastRobotSection && ROBOT_MSGS[current]) {
    lastRobotSection = current;
    showRobotBubble(ROBOT_MSGS[current]);
  }
}

window.addEventListener('scroll', checkRobotSection, { passive: true });

// Show welcome message after 2 seconds
setTimeout(() => {
  showRobotBubble("Hi! I'm Karib's AI Robot Guide 🤖 Click me to chat!");
}, 2000);

// Send message in robot chat
async function sendRobotMsg() {
  const inp = document.getElementById('rcInput');
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = '';

  addRobotMsg(msg, 'user');
  const tid = 'rt' + Date.now();
  addRobotTyping(tid);

  try {
    const res = await fetch('/api/chat/', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body:    JSON.stringify({ message: msg }),
    });
    const data = await res.json();
    removeRobotTyping(tid);
    addRobotMsg(data.reply || 'No response.', 'bot');
  } catch {
    removeRobotTyping(tid);
    addRobotMsg('Connection error. Please try again.', 'bot');
  }
}

function addRobotMsg(text, role) {
  const wrap = document.getElementById('rcMessages');
  const d    = document.createElement('div');
  d.className = 'rc-msg ' + role;
  const fmt = esc(text).replace(/\n/g, '<br/>');
  d.innerHTML = `<div class="rc-bubble">${fmt}</div>`;
  wrap.appendChild(d);
  wrap.scrollTop = wrap.scrollHeight;
}

function addRobotTyping(id) {
  const wrap = document.getElementById('rcMessages');
  const d    = document.createElement('div');
  d.className = 'rc-msg bot'; d.id = id;
  d.innerHTML = '<div class="rc-bubble"><span class="typing-dots"><span>●</span><span>●</span><span>●</span></span></div>';
  wrap.appendChild(d);
  wrap.scrollTop = wrap.scrollHeight;
}

function removeRobotTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// Enter key to send
document.getElementById('rcInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') sendRobotMsg();
});

// Robot body hover — stop floating
document.getElementById('robot-body').addEventListener('mouseenter', () => {
  document.getElementById('robot-body').style.animationPlayState = 'paused';
});
document.getElementById('robot-body').addEventListener('mouseleave', () => {
  document.getElementById('robot-body').style.animationPlayState = 'running';
});

/* ═══════════════════════════════════════════════
   DATA VISUALISATION — Chart.js
═══════════════════════════════════════════════ */

// Chart default styles
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'JetBrains Mono', monospace";
Chart.defaults.font.size = 11;

const ACC  = '#00FFC2';
const ACC2 = '#22D3EE';
const GOLD = '#F59E0B';
const SEC  = '#64748B';
const CARD = 'rgba(36,43,54,0.8)';

let chartsInitialised = false;

function initCharts() {
  if (chartsInitialised) return;
  chartsInitialised = true;

  // ── CHART 1: Publications by Year ──────────
  new Chart(document.getElementById('chartYear'), {
    type: 'bar',
    data: {
      labels: ['2024', '2025', '2026'],
      datasets: [{
        label: 'Papers Published',
        data: [1, 13, 2],
        backgroundColor: [
          'rgba(0,255,194,.2)',
          'rgba(0,255,194,.6)',
          'rgba(34,211,238,.4)',
        ],
        borderColor: [ACC, ACC, ACC2],
        borderWidth: 2,
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#242b36',
          borderColor: ACC,
          borderWidth: 1,
          callbacks: {
            label: ctx => ` ${ctx.parsed.y} paper${ctx.parsed.y>1?'s':''}`,
          },
        },
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#94a3b8' } },
        y: { grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#94a3b8', stepSize: 1 }, beginAtZero: true },
      },
      animation: { duration: 1200, easing: 'easeOutQuart' },
    },
  });

  // ── CHART 2: Publications by Venue ─────────
  new Chart(document.getElementById('chartVenue'), {
    type: 'doughnut',
    data: {
      labels: ['IEEE', 'Springer', 'Elsevier / Data in Brief', 'Nature Portfolio'],
      datasets: [{
        data: [7, 3, 4, 2],
        backgroundColor: [
          'rgba(0,255,194,.7)',
          'rgba(34,211,238,.7)',
          'rgba(245,158,11,.7)',
          'rgba(100,116,139,.7)',
        ],
        borderColor: ['#1a1e23'],
        borderWidth: 3,
        hoverOffset: 8,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#94a3b8', padding: 12, font: { size: 10 } },
        },
        tooltip: {
          backgroundColor: '#242b36',
          borderColor: ACC,
          borderWidth: 1,
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed} papers`,
          },
        },
      },
      animation: { duration: 1200, easing: 'easeOutQuart' },
    },
  });

  // ── CHART 3: Research Topics ────────────────
  new Chart(document.getElementById('chartTopics'), {
    type: 'bar',
    data: {
      labels: ['Medical AI', 'Agriculture AI', 'XAI', 'NLP / Emotion', 'Computer Vision', 'Datasets'],
      datasets: [{
        label: 'Papers',
        data: [5, 5, 2, 2, 2, 4],
        backgroundColor: [
          'rgba(0,255,194,.55)',
          'rgba(34,211,238,.55)',
          'rgba(245,158,11,.55)',
          'rgba(0,255,194,.35)',
          'rgba(34,211,238,.35)',
          'rgba(100,116,139,.55)',
        ],
        borderColor: [ACC, ACC2, GOLD, ACC, ACC2, SEC],
        borderWidth: 2,
        borderRadius: 6,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#242b36',
          borderColor: ACC,
          borderWidth: 1,
          callbacks: {
            label: ctx => ` ${ctx.parsed.x} paper${ctx.parsed.x>1?'s':''}`,
          },
        },
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#94a3b8', stepSize: 1 }, beginAtZero: true },
        y: { grid: { color: 'rgba(255,255,255,.03)' }, ticks: { color: '#94a3b8' } },
      },
      animation: { duration: 1200, easing: 'easeOutQuart' },
    },
  });

  // ── CHART 4: Citations per Paper ────────────
  new Chart(document.getElementById('chartCitations'), {
    type: 'bar',
    data: {
      labels: ['TFP-BD', 'Sunflower', 'TB Diagnosis', 'Mushroom XAI', 'Drug XAI', 'BDFlower', 'Vegetable'],
      datasets: [{
        label: 'Citations',
        data: [2, 2, 1, 1, 1, 1, 1],
        backgroundColor: 'rgba(245,158,11,.5)',
        borderColor: GOLD,
        borderWidth: 2,
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#242b36',
          borderColor: GOLD,
          borderWidth: 1,
          callbacks: {
            label: ctx => ` ${ctx.parsed.y} citation${ctx.parsed.y>1?'s':''}`,
          },
        },
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#94a3b8', maxRotation: 30 } },
        y: { grid: { color: 'rgba(255,255,255,.05)' }, ticks: { color: '#94a3b8', stepSize: 1 }, beginAtZero: true },
      },
      animation: { duration: 1200, easing: 'easeOutQuart' },
    },
  });
}

// Init charts when section scrolls into view
const vizObs = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    initCharts();
    vizObs.disconnect();
  }
}, { threshold: .1 });

const vizSection = document.getElementById('dataviz');
if (vizSection) vizObs.observe(vizSection);

/* ═══════════════════════════════════════════════
   SKILL RADAR CHART
═══════════════════════════════════════════════ */
function initRadar() {
  const ctx = document.getElementById('skillRadar');
  if (!ctx || ctx.dataset.init) return;
  ctx.dataset.init = '1';

  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Deep Learning', 'Computer Vision', 'NLP', 'RAG Systems', 'XAI', 'Automation', 'Python', 'Research'],
      datasets: [{
        label: 'Karib Shams',
        data: [95, 90, 88, 92, 85, 87, 96, 94],
        backgroundColor: 'rgba(0,255,194,.12)',
        borderColor: '#00FFC2',
        borderWidth: 2,
        pointBackgroundColor: '#00FFC2',
        pointBorderColor: '#1a1e23',
        pointBorderWidth: 2,
        pointRadius: 4,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#242b36',
          borderColor: '#00FFC2',
          borderWidth: 1,
        },
      },
      scales: {
        r: {
          min: 60, max: 100,
          grid:      { color: 'rgba(255,255,255,.08)' },
          angleLines:{ color: 'rgba(255,255,255,.08)' },
          pointLabels:{ color: '#94a3b8', font: { size: 10 } },
          ticks: { display: false },
        },
      },
      animation: { duration: 1400, easing: 'easeOutQuart' },
    },
  });
}

// Animate progress bars
function animateProgressBars() {
  document.querySelectorAll('.pb-fill').forEach(bar => {
    const w = bar.dataset.width;
    setTimeout(() => { bar.style.width = w + '%'; }, 200);
  });
}

// Observe skills section for radar + bars
const skillObs = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    initRadar();
    animateProgressBars();
    skillObs.disconnect();
  }
}, { threshold: .15 });
const skillSec = document.getElementById('skills');
if (skillSec) skillObs.observe(skillSec);

/* ═══════════════════════════════════════════════
   GAME SWITCHER
═══════════════════════════════════════════════ */
function switchGame(name) {
  document.querySelectorAll('.game-panel').forEach(p => p.classList.add('hidden'));
  document.querySelectorAll('.gtab').forEach(t => t.classList.remove('active'));
  document.getElementById('game-' + name).classList.remove('hidden');
  event.target.classList.add('active');
}

/* ═══════════════════════════════════════════════
   GAME 2 — GUESS THE AI MODEL
═══════════════════════════════════════════════ */
const GUESS_QS = [
  { clue: "I process images by sliding small filters across them, learning edges, textures, and shapes layer by layer. I'm the backbone of most image recognition systems.", opts: ["LSTM", "CNN", "Random Forest", "XGBoost"], a: 1 },
  { clue: "I read a sentence from both left to right AND right to left simultaneously. I'm pre-trained on masked words. I revolutionised NLP in 2018.", opts: ["GPT-2", "BERT", "T5", "XLNet"], a: 1 },
  { clue: "I can detect multiple objects in an image in a single forward pass. My name literally means I look at the whole image just once.", opts: ["Faster R-CNN", "SSD", "YOLO", "RetinaNet"], a: 2 },
  { clue: "I use Shapley values from game theory to explain exactly how much each feature contributed to a model's prediction.", opts: ["LIME", "SHAP", "Grad-CAM", "Anchors"], a: 1 },
  { clue: "I retrieve relevant documents first, then feed them to a language model to generate grounded, factual answers. I reduce hallucinations dramatically.", opts: ["Fine-tuning", "RAG", "Prompt Chaining", "In-context Learning"], a: 1 },
  { clue: "I'm a vision transformer that uses shifted windows for attention computation, giving me linear complexity and hierarchical features like CNNs.", opts: ["ViT", "DeiT", "Swin Transformer", "BEiT"], a: 2 },
  { clue: "I'm an ensemble of hundreds of decision trees. Each tree sees a random subset of data and features. I combine their votes for the final answer.", opts: ["XGBoost", "AdaBoost", "Random Forest", "Bagging Classifier"], a: 2 },
  { clue: "I'm a self-supervised learning framework where I learn by comparing augmented views of the same image, pulling similar pairs together and pushing different pairs apart.", opts: ["MAE", "SimCLR", "DINO", "MoCo"], a: 1 },
  { clue: "I'm an open-source workflow automation tool. I connect APIs, AI models, and databases using visual nodes — no heavy coding needed.", opts: ["Zapier", "n8n", "Airflow", "Prefect"], a: 1 },
  { clue: "I'm a gradient boosted tree algorithm optimised for speed and performance. I handle missing data automatically and have built-in regularisation.", opts: ["Random Forest", "LightGBM", "XGBoost", "CatBoost"], a: 2 },
];

let gIdx = 0, gScore = 0, gQs = [];

function initGuessGame() {
  gQs = shuffle([...GUESS_QS]);
  gIdx = 0; gScore = 0;
  document.getElementById('guessStartBtn').style.display = 'none';
  document.getElementById('guessScore').textContent = 'Score: 0/' + gQs.length;
  showGuessQ();
}

function showGuessQ() {
  if (gIdx >= gQs.length) {
    const pct = Math.round((gScore / gQs.length) * 100);
    document.getElementById('guessClue').innerHTML = `<strong style="color:var(--acc)">Game Over! Score: ${gScore}/${gQs.length} (${pct}%)</strong>`;
    document.getElementById('guessOpts').innerHTML = '';
    document.getElementById('guessScore').textContent = pct >= 80 ? '🏆 AI Expert!' : pct >= 60 ? '⭐ Great!' : '📚 Keep Learning!';
    const btn = document.getElementById('guessStartBtn');
    btn.textContent = 'Play Again';
    btn.style.display = 'inline-flex';
    return;
  }
  const q = gQs[gIdx];
  document.getElementById('guessClue').textContent = q.clue;
  const oe = document.getElementById('guessOpts'); oe.innerHTML = '';
  q.opts.forEach((opt, i) => {
    const b = document.createElement('button');
    b.className = 'guess-opt'; b.textContent = opt;
    b.onclick = () => {
      Array.from(oe.children).forEach(x => x.disabled = true);
      if (i === q.a) { b.classList.add('correct'); gScore++; }
      else { b.classList.add('wrong'); oe.children[q.a].classList.add('correct'); }
      document.getElementById('guessScore').textContent = 'Score: ' + gScore + '/' + gQs.length;
      gIdx++;
      setTimeout(showGuessQ, 1200);
    };
    oe.appendChild(b);
  });
}

/* ═══════════════════════════════════════════════
   GAME 3 — PREDICT THE OUTPUT
═══════════════════════════════════════════════ */
const PREDICT_QS = [
  { clue: "You train a model with 10,000 features but only 100 training samples. The training accuracy is 99%. What happens on the test set?", opts: ["High accuracy — model is great", "Low accuracy — model overfits", "Same accuracy as training", "Model refuses to train"], a: 1 },
  { clue: "You use a learning rate of 10.0 (very large) in gradient descent. What happens to the loss?", opts: ["Converges quickly to minimum", "Diverges — loss explodes or oscillates", "Stays the same", "Gradually decreases"], a: 1 },
  { clue: "Your dataset has 95% class A and 5% class B. You train a model that always predicts class A. What is the accuracy?", opts: ["50%", "5%", "95%", "100%"], a: 2 },
  { clue: "You apply dropout with rate 0.9 (90% neurons dropped) during training. What is the likely result?", opts: ["Perfect regularisation", "Severe underfitting — model can't learn", "Faster training", "Better generalisation"], a: 1 },
  { clue: "You add 50 more layers to a deep neural network without residual connections. Training accuracy starts dropping. This is called:", opts: ["Overfitting", "Vanishing gradient problem", "Data leakage", "Mode collapse"], a: 1 },
  { clue: "You have a RAG system but the retrieved documents are always irrelevant to the question. What is the likely problem?", opts: ["LLM is too small", "Poor embedding model or chunking strategy", "Too many documents", "Wrong temperature setting"], a: 1 },
  { clue: "You train YOLO on 10,000 images of cars in daylight. At night, detection fails completely. This is called:", opts: ["Overfitting", "Distribution shift / domain mismatch", "Low learning rate", "Wrong architecture"], a: 1 },
  { clue: "In a GAN, the discriminator becomes perfect too quickly and the generator stops improving. This is called:", opts: ["Vanishing gradient", "Mode collapse", "Discriminator dominance", "Training collapse"], a: 2 },
];

let pIdx = 0, pScore = 0, pQs = [];

function initPredictGame() {
  pQs = shuffle([...PREDICT_QS]);
  pIdx = 0; pScore = 0;
  document.getElementById('predictStartBtn').style.display = 'none';
  document.getElementById('predictScore').textContent = 'Score: 0/' + pQs.length;
  showPredictQ();
}

function showPredictQ() {
  if (pIdx >= pQs.length) {
    const pct = Math.round((pScore / pQs.length) * 100);
    document.getElementById('predictClue').innerHTML = `<strong style="color:var(--acc)">Done! Score: ${pScore}/${pQs.length} (${pct}%)</strong>`;
    document.getElementById('predictOpts').innerHTML = '';
    document.getElementById('predictScore').textContent = pct >= 80 ? '🏆 ML Expert!' : pct >= 60 ? '⭐ Good thinking!' : '📚 Study more ML!';
    const btn = document.getElementById('predictStartBtn');
    btn.textContent = 'Play Again';
    btn.style.display = 'inline-flex';
    return;
  }
  const q = pQs[pIdx];
  document.getElementById('predictClue').textContent = q.clue;
  const oe = document.getElementById('predictOpts'); oe.innerHTML = '';
  q.opts.forEach((opt, i) => {
    const b = document.createElement('button');
    b.className = 'guess-opt'; b.textContent = opt;
    b.onclick = () => {
      Array.from(oe.children).forEach(x => x.disabled = true);
      if (i === q.a) { b.classList.add('correct'); pScore++; }
      else { b.classList.add('wrong'); oe.children[q.a].classList.add('correct'); }
      document.getElementById('predictScore').textContent = 'Score: ' + pScore + '/' + pQs.length;
      pIdx++;
      setTimeout(showPredictQ, 1200);
    };
    oe.appendChild(b);
  });
}

/* ═══════════════════════════════════════════════
   LIVE RESEARCH IMPACT COUNTERS
═══════════════════════════════════════════════ */
const IMPACT_DATA = [
  { id: 'imp1', target: 16, suffix: '+' },
  { id: 'imp2', target: 9,  suffix: ''  },
  { id: 'imp3', target: 2,  suffix: ''  },
  { id: 'imp4', target: 1,  suffix: ''  },
  { id: 'imp5', target: 60, suffix: '+' },
  { id: 'imp6', target: 4,  suffix: ''  },
];

function animateImpactCounters() {
  IMPACT_DATA.forEach(({ id, target, suffix }) => {
    const el = document.getElementById(id);
    if (!el) return;
    let cur = 0;
    const step = target / 50;
    const timer = setInterval(() => {
      cur += step;
      if (cur >= target) {
        el.textContent = target + suffix;
        clearInterval(timer);
      } else {
        el.textContent = Math.floor(cur) + suffix;
      }
    }, 35);
  });
}

const impactObs = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    animateImpactCounters();
    impactObs.disconnect();
  }
}, { threshold: .2 });

const impactSec = document.getElementById('impact');
if (impactSec) impactObs.observe(impactSec);

/* ═══════════════════════════════════════════════
   ROBOT MSG FOR NEW SECTIONS
═══════════════════════════════════════════════ */
ROBOT_MSGS['timeline'] = "⭐ This is Karib's journey — from GPA 5.00 in SSC all the way to Best Paper Award in Washington D.C.!";
ROBOT_MSGS['impact']   = "📈 16 papers, 9 citations, h-index 2, and 60+ AI products — Karib's research impact in numbers!";

/* ═══════════════════════════════════════════════
   P5: DARK / LIGHT MODE TOGGLE
═══════════════════════════════════════════════ */
function toggleTheme() {
  const body = document.body;
  const btn  = document.getElementById('themeToggle');
  const isLight = body.classList.toggle('light-mode');
  btn.textContent = isLight ? '☀️' : '🌙';
  btn.title = isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode';
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
}
(function applySavedTheme() {
  const saved = localStorage.getItem('theme');
  if (saved === 'light') {
    document.body.classList.add('light-mode');
    const btn = document.getElementById('themeToggle');
    if (btn) { btn.textContent = '☀️'; btn.title = 'Switch to Dark Mode'; }
  }
})();

/* ═══════════════════════════════════════════════
   P6: VISITOR COUNTER (display only — backend handles counting)
═══════════════════════════════════════════════ */
// Counters are rendered server-side via Django template

/* ═══════════════════════════════════════════════
   P7: TYPING SPEED GAME
═══════════════════════════════════════════════ */
const TYPING_WORDS = [
  'neural','network','machine','learning','deep','python',
  'transformer','attention','embedding','dataset','training',
  'gradient','backprop','dropout','softmax','sigmoid','relu',
  'convolution','pooling','encoder','decoder','tokenizer',
  'classification','regression','clustering','overfitting',
  'accuracy','precision','recall','xgboost','random','forest',
  'ensemble','boosting','computer','vision','yolo','detection',
  'segmentation','language','model','chatbot','inference',
  'pipeline','retrieval','augmented','generation','vector',
  'explainable','shapley','interpretable','karib','aistream',
];

let tgWords=[], tgIdx=0, tgCorrect=0, tgWrong=0;
let tgTimer=null, tgTimeLeft=30, tgActive=false;

function startTypingGame() {
  tgWords=shuffle([...TYPING_WORDS]);
  tgIdx=0; tgCorrect=0; tgWrong=0; tgTimeLeft=30; tgActive=true;
  document.getElementById('tgStartBtn').style.display='none';
  document.getElementById('tgResult').textContent='';
  document.getElementById('tgInput').disabled=false;
  document.getElementById('tgInput').value='';
  document.getElementById('tgInput').focus();
  document.getElementById('tgProgFill').style.width='100%';
  updateTgStats(); showTgWord();
  tgTimer=setInterval(()=>{
    tgTimeLeft--;
    document.getElementById('tgTime').textContent=tgTimeLeft;
    document.getElementById('tgProgFill').style.width=(tgTimeLeft/30*100)+'%';
    if(tgTimeLeft<=0) endTypingGame();
  },1000);
}
function showTgWord() {
  if(tgIdx>=tgWords.length) tgIdx=0;
  const d=document.getElementById('tgWordDisplay');
  d.textContent=tgWords[tgIdx]; d.className='tg-word-display';
}
function updateTgStats() {
  const elapsed=30-tgTimeLeft;
  const wpm=elapsed>0?Math.round((tgCorrect/elapsed)*60):0;
  const total=tgCorrect+tgWrong;
  const acc=total>0?Math.round((tgCorrect/total)*100):100;
  document.getElementById('tgWpm').textContent=wpm;
  document.getElementById('tgAcc').textContent=acc;
  document.getElementById('tgScore').textContent=tgCorrect;
}
function endTypingGame() {
  clearInterval(tgTimer); tgActive=false;
  document.getElementById('tgInput').disabled=true;
  const wpm=Math.round((tgCorrect/30)*60);
  const total=tgCorrect+tgWrong;
  const acc=total>0?Math.round((tgCorrect/total)*100):0;
  const grade=wpm>=60?'🏆 Expert!':wpm>=40?'⭐ Great!':wpm>=20?'👍 Good!':'📚 Keep Practicing!';
  document.getElementById('tgResult').textContent=`${grade} WPM:${wpm} · Accuracy:${acc}% · Words:${tgCorrect}`;
  document.getElementById('tgWordDisplay').textContent='Game Over!';
  const btn=document.getElementById('tgStartBtn');
  btn.textContent='🔄 Play Again'; btn.style.display='inline-flex';
}
const tgInputEl=document.getElementById('tgInput');
if(tgInputEl){
  tgInputEl.addEventListener('input',function(){
    if(!tgActive) return;
    const typed=this.value.trim().toLowerCase();
    const target=tgWords[tgIdx].toLowerCase();
    const d=document.getElementById('tgWordDisplay');
    if(typed===target){
      tgCorrect++; tgIdx++; this.value='';
      d.className='tg-word-display correct';
      showTgWord(); updateTgStats();
    } else if(target.startsWith(typed)){
      d.className='tg-word-display';
    } else {
      d.className='tg-word-display wrong';
    }
  });
}

/* ═══════════════════════════════════════════════
   P8: MOBILE APP FEEL
═══════════════════════════════════════════════ */
// Bottom nav active state
function setMbnActive(el) {
  document.querySelectorAll('.mbn-item').forEach(i=>i.classList.remove('active'));
  el.classList.add('active');
}

// Update bottom nav on scroll
window.addEventListener('scroll', () => {
  let cur = '';
  document.querySelectorAll('section[id]').forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) cur = s.id;
  });
  const map = { hero:'#hero', about:'#hero', skills:'#hero', projects:'#projects', publications:'#publications', aichat:'#aichat', contact:'#contact' };
  const href = map[cur] || '#hero';
  document.querySelectorAll('.mbn-item').forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === href);
  });
}, { passive: true });

// Swipe gestures between sections
let touchStartY = 0, touchStartX = 0;
document.addEventListener('touchstart', e => {
  touchStartY = e.touches[0].clientY;
  touchStartX = e.touches[0].clientX;
}, { passive: true });

document.addEventListener('touchend', e => {
  const dy = touchStartY - e.changedTouches[0].clientY;
  const dx = touchStartX - e.changedTouches[0].clientX;
  if (Math.abs(dy) > Math.abs(dx) && Math.abs(dy) > 60) {
    // Vertical swipe — natural scroll, handled by browser
  }
}, { passive: true });

// Pull to refresh
let pullStart = 0, pulling = false;
const pullEl = document.getElementById('pullRefresh');

document.addEventListener('touchstart', e => {
  if (window.scrollY === 0) { pullStart = e.touches[0].clientY; pulling = true; }
}, { passive: true });

document.addEventListener('touchmove', e => {
  if (!pulling || !pullEl) return;
  const dist = e.touches[0].clientY - pullStart;
  if (dist > 80) {
    pullEl.classList.add('visible');
    if (pullEl) pullEl.style.display = 'block';
  }
}, { passive: true });

document.addEventListener('touchend', () => {
  if (!pullEl) return;
  const wasVisible = pullEl.classList.contains('visible');
  pullEl.classList.remove('visible');
  setTimeout(() => { if(pullEl) pullEl.style.display='none'; }, 300);
  if (wasVisible) setTimeout(() => location.reload(), 400);
  pulling = false;
}, { passive: true });

// CV Download animation
const cvBtn = document.getElementById('cvDownloadBtn');
if (cvBtn) {
  cvBtn.addEventListener('click', () => {
    const main = cvBtn.querySelector('.cv-main');
    const arrow = cvBtn.querySelector('.cv-arrow');
    if (!main || !arrow) return;
    main.textContent = 'Downloading...';
    arrow.textContent = '✓';
    cvBtn.style.borderColor = '#22c55e';
    setTimeout(() => {
      main.textContent = 'Download CV';
      arrow.textContent = '↓';
      cvBtn.style.borderColor = '';
    }, 2500);
  });
}

// Journey animation
const journeyObs2 = new IntersectionObserver(entries => {
  if (entries[0].isIntersecting) {
    setTimeout(() => {
      const fill = document.getElementById('jpFill');
      if (fill) fill.style.width = '100%';
    }, 300);
    journeyObs2.disconnect();
  }
}, { threshold: .1 });
const journeySec2 = document.getElementById('timeline');
if (journeySec2) journeyObs2.observe(journeySec2);

document.querySelectorAll('.journey-card').forEach(card => {
  const o = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) { card.classList.add('vis'); o.disconnect(); }
  }, { threshold: .2 });
  o.observe(card);
});

/* ═══════════════════════════════════════════════
   P9: 3D PARTICLES (Three.js)
═══════════════════════════════════════════════ */
(function init3D() {
  if (typeof THREE === 'undefined') return;

  const canvas3d = document.getElementById('three-canvas');
  if (!canvas3d) return;

  const renderer = new THREE.WebGLRenderer({ canvas: canvas3d, alpha: true, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.z = 5;

  // Create particles
  const count = 1200;
  const geo   = new THREE.BufferGeometry();
  const pos   = new Float32Array(count * 3);
  const col   = new Float32Array(count * 3);

  for (let i = 0; i < count; i++) {
    pos[i*3]   = (Math.random()-0.5) * 20;
    pos[i*3+1] = (Math.random()-0.5) * 20;
    pos[i*3+2] = (Math.random()-0.5) * 20;
    // Neon cyan / teal colours
    const r = Math.random();
    if (r < 0.5) {
      col[i*3]=0; col[i*3+1]=1; col[i*3+2]=0.76; // #00FFC2
    } else {
      col[i*3]=0.13; col[i*3+1]=0.83; col[i*3+2]=0.93; // #22D3EE
    }
  }

  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color',    new THREE.BufferAttribute(col, 3));

  const mat = new THREE.PointsMaterial({
    size: 0.04,
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    sizeAttenuation: true,
  });

  const particles = new THREE.Points(geo, mat);
  scene.add(particles);

  // Mouse influence
  let mouseX = 0, mouseY = 0;
  document.addEventListener('mousemove', e => {
    mouseX = (e.clientX / window.innerWidth  - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // Show Three.js canvas, hide old neural canvas
  canvas3d.classList.add('active');
  document.body.classList.add('three-active');

  let t = 0;
  (function animate3d() {
    requestAnimationFrame(animate3d);
    t += 0.003;
    particles.rotation.y = t * 0.15 + mouseX * 0.1;
    particles.rotation.x = t * 0.08 + mouseY * 0.05;
    // Gentle pulsing scale
    const scale = 1 + Math.sin(t * 1.5) * 0.02;
    particles.scale.set(scale, scale, scale);
    renderer.render(scene, camera);
  })();
})();

/* ═══════════════════════════════════════════════
   P9: PAGE TRANSITION ON LOAD
═══════════════════════════════════════════════ */
(function pageTransitionInit() {
  const overlay = document.getElementById('pageTransition');
  if (!overlay) return;

  // Entry animation — slide out on load
  overlay.classList.add('active');
  requestAnimationFrame(() => {
    setTimeout(() => {
      overlay.classList.remove('active');
      overlay.classList.add('exit');
      setTimeout(() => { overlay.classList.remove('exit'); }, 600);
    }, 100);
  });

  // Exit animation on nav link clicks
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', () => {
      // Subtle flash effect on internal links
      overlay.style.background = 'linear-gradient(135deg,rgba(0,255,194,.08),transparent)';
      overlay.classList.add('active');
      setTimeout(() => { overlay.classList.remove('active'); }, 250);
    });
  });
})();

/* ═══════════════════════════════════════════════
   GAME SWITCHER (handles all 4 games)
═══════════════════════════════════════════════ */
function switchGame(name) {
  document.querySelectorAll('.game-panel').forEach(p => p.classList.add('hidden'));
  document.querySelectorAll('.gtab').forEach(t => t.classList.remove('active'));
  const panel = document.getElementById('game-' + name);
  if (panel) panel.classList.remove('hidden');
  if (event && event.target) event.target.classList.add('active');
  // Stop typing game if switching away
  if (name !== 'typing' && tgActive) { clearInterval(tgTimer); tgActive = false; }
}

/* ═══════════════════════════════════════════════
   TEXT-TO-SPEECH — Robot Voice
═══════════════════════════════════════════════ */
let robotMuted = false;

function toggleMute() {
  robotMuted = !robotMuted;
  const btn = document.getElementById('muteBtn');
  if (btn) btn.textContent = robotMuted ? '🔇' : '🔊';
  if (robotMuted && window.speechSynthesis) window.speechSynthesis.cancel();
}

function speakText(text) {
  if (!window.speechSynthesis || robotMuted) return;
  window.speechSynthesis.cancel();

  // Clean text — remove emojis and symbols
  const clean = text
    .replace(/[^\w\s,.!?'-]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 250);

  if (!clean) return;

  const utter = new SpeechSynthesisUtterance(clean);
  utter.rate   = 0.92;
  utter.pitch  = 1.0;
  utter.volume = 1.0;
  utter.lang   = 'en-US';

  const speak = () => {
    const voices = window.speechSynthesis.getVoices();
    const voice  = voices.find(v => v.lang === 'en-US' && v.name.includes('Google'))
                || voices.find(v => v.lang === 'en-US')
                || voices.find(v => v.lang.startsWith('en'))
                || null;
    if (voice) utter.voice = voice;
    setTimeout(() => window.speechSynthesis.speak(utter), 100);
  };

  const voices = window.speechSynthesis.getVoices();
  if (voices.length > 0) {
    speak();
  } else {
    window.speechSynthesis.onvoiceschanged = () => {
      window.speechSynthesis.onvoiceschanged = null;
      speak();
    };
  }
}

// Pre-load voices on page load (Chrome fix)
window.addEventListener('load', () => {
  if (window.speechSynthesis) window.speechSynthesis.getVoices();
});

// Override addRobotMsg to speak bot replies
const _origAddRobotMsg = addRobotMsg;
// Patch: speak when bot replies in robot chat
const origSendRobotMsg = sendRobotMsg;
async function sendRobotMsg() {
  const inp = document.getElementById('rcInput');
  const msg = inp.value.trim();
  if (!msg) return;
  inp.value = '';

  addRobotMsg(msg, 'user');
  const tid = 'rt' + Date.now(); addRobotTyping(tid);

  try {
    const res = await fetch('/api/chat/', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body:    JSON.stringify({ message: msg }),
    });
    const data = await res.json();
    removeRobotTyping(tid);
    const reply = data.reply || 'No response.';
    addRobotMsg(reply, 'bot');
    speakText(reply); // 🔊 SPEAK the reply
  } catch {
    removeRobotTyping(tid);
    addRobotMsg('Connection error. Please try again.', 'bot');
  }
}

// Re-bind Enter key for robot chat
const rcInputEl = document.getElementById('rcInput');
if (rcInputEl) {
  // Remove old listener by cloning
  const newRcInput = rcInputEl.cloneNode(true);
  rcInputEl.parentNode.replaceChild(newRcInput, rcInputEl);
  newRcInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendRobotMsg();
  });
}

/* ── LUCIDE ICONS INIT ── */
if (typeof lucide !== 'undefined') lucide.createIcons();