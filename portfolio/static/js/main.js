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

  // 🔊 Speak bot replies
  if (role === 'bot') {
    speakText(text);
  }
}

function speakText(text) {
  if (!window.speechSynthesis || robotMuted) return;

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  // Clean text
  const clean = text
    .replace(/[^\w\s,.!?'-]/g, '')
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

    // Chrome bug — needs small delay
    setTimeout(() => {
      window.speechSynthesis.speak(utter);
    }, 100);
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
let robotMuted = false;
function toggleMute() {
  robotMuted = !robotMuted;
  document.getElementById('muteBtn').textContent = robotMuted ? '🔇' : '🔊';
  if (robotMuted) window.speechSynthesis.cancel();
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
// Pre-load voices on page load
window.addEventListener('load', () => {
  if (window.speechSynthesis) {
    window.speechSynthesis.getVoices();
  }
});