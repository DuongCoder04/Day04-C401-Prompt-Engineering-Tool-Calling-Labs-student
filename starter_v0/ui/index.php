<?php $year = date('Y'); ?>
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Research Agent — AI Assistant Toolkit</title>
  <meta name="description" content="Modular AI research agent with 14 tools: Twitter, web search, news, papers, calculator, music, stories, Telegram, and more. Open-source.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="landing.css">
  <style>
    /* live chat embed */
    .chat-frame {
      width: 100%;
      border: none;
      border-radius: var(--radius);
      background: #fff;
      min-height: 480px;
      box-shadow: 0 4px 24px rgba(0,0,0,0.04);
    }
    .chat-link {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 12px 24px;
      background: var(--accent);
      color: #fff;
      border-radius: var(--radius);
      text-decoration: none;
      font-size: 14px;
      transition: all 0.2s;
    }
    .chat-link:hover { background: var(--accent-hover); transform: translateY(-1px); }
    .chat-link .arrow { transition: transform 0.2s; }
    .chat-link:hover .arrow { transform: translateX(4px); }
    .code-snippet {
      font-family: var(--font-mono);
      font-size: 13px;
      background: var(--bg-alt);
      padding: 12px 16px;
      border-radius: var(--radius);
      color: var(--text-muted);
      border: 1px solid var(--border);
    }
  </style>
</head>
<body>

<nav id="nav">
  <a href="#" class="logo">Research<span>Agent</span></a>
  <ul class="nav-links">
    <li><a href="#demo">Demo</a></li>
    <li><a href="https://github.com/your-org/research-agent" target="_blank">GitHub</a></li>
    <li><a href="#chat" class="btn-ghost">Try Chat</a></li>
  </ul>
</nav>

<!-- Hero -->
<section class="hero" id="hero">
  <div class="hero-inner">
    <div class="hero-text">
      <div class="hero-badge reveal">Open Source</div>
      <h1 class="reveal reveal-delay-1">Research<br>Agent</h1>
      <p class="reveal reveal-delay-2">Modular AI toolkit with live chat. One agent, multiple tools — extensible and eval-driven.</p>
      <div class="code-snippet reveal reveal-delay-3" style="margin-bottom:36px;">
        <span style="color:var(--orange);">$</span> python chat.py --query "Tim tin AI hom nay"
      </div>
      <div class="trust-bar reveal reveal-delay-4">
        <div class="stat">
          <span class="num">4</span>
          <span class="label">eval suites</span>
        </div>
        <div class="avatars">
          <div class="dot">T</div>
          <div class="dot">W</div>
          <div class="dot">P</div>
          <div class="dot">M</div>
          <div class="dot">S</div>
        </div>
        <span class="trust-text">Tools · Web · Papers · Music · Stories</span>
      </div>
    </div>

    <div class="hero-carousel-container">
      <div class="carousel-stage" id="carouselStage">
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/calculate/800/600" alt="" draggable="false"></figure>
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/websearch/800/600" alt="" draggable="false"></figure>
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/music/800/600" alt="" draggable="false"></figure>
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/stories/800/600" alt="" draggable="false"></figure>
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/chat/800/600" alt="" draggable="false"></figure>
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/data/800/600" alt="" draggable="false"></figure>
        <figure class="hero-3d-slide"><img src="https://picsum.photos/seed/tools/800/600" alt="" draggable="false"></figure>
      </div>
      <div class="hero-3d-dots">
        <span class="active" data-i="0"></span><span data-i="1"></span><span data-i="2"></span><span data-i="3"></span><span data-i="4"></span><span data-i="5"></span><span data-i="6"></span>
      </div>
    </div>
  </div>
</section>

<!-- Demo -->
<section class="section demo-section" id="demo">
  <div class="demo-content">
    <div class="demo-text reveal">
      <div class="badge">Interactive</div>
      <h2>Try the agent live</h2>
      <p>Full agent loop: route → call tool → return result. Supports multi-turn, parallel tool calls, and eval-driven development.</p>
      <ul style="margin:16px 0;padding-left:18px;color:var(--text-muted);font-size:14px;line-height:1.8;">
        <li>Twitter timeline + search</li>
        <li>Web lookup + news tracking</li>
        <li>ArXiv paper search + full-text</li>
        <li>Calculator (handles ×, ÷, sqrt)</li>
        <li>Music &amp; story discovery APIs</li>
        <li>Telegram sending + policy lookup</li>
      </ul>
      <a href="#chat" class="chat-link">Open Chat <span class="arrow">→</span></a>
    </div>

    <div class="mockup reveal reveal-delay-2">
      <div class="mockup-header">
        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        <span>agent — interactive</span>
      </div>
      <div class="mockup-body" style="padding:20px 24px;">
        <div class="cli-showcase" id="cliDemo">
          <div class="cli-line"><span class="arrow">→</span> <span>Research Agent initialized</span></div>
          <div class="cli-line"><span class="arrow">→</span> <span class="output">Loaded 14 tool definitions</span></div>
          <div class="cli-line"><span class="arrow">→</span> <span class="output">System prompt: routing rules loaded</span></div>
          <div class="cli-line"><span class="arrow">→</span> <span class="highlight">Ready. Type your query below.</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Chat -->
<section class="cta-section" id="chat" style="padding:80px 28px 100px;">
  <h2 class="reveal">Talk to the agent</h2>
  <p class="reveal reveal-delay-1" style="margin-bottom:32px;">Ask it anything — it will route to the right tool automatically.</p>
  <div class="reveal reveal-delay-2" style="max-width:720px;margin:0 auto;">
    <div class="mockup" style="text-align:left;">
      <div class="mockup-header">
        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        <span>chat.research</span>
      </div>
      <div class="mockup-body" id="chatBody" style="padding:0;background:var(--bg);">
        <div id="chatMessages" style="padding:20px;max-height:360px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;font-size:14px;line-height:1.6;">
          <div style="display:flex;gap:8px;align-items:flex-start;">
            <div style="width:24px;height:24px;border-radius:50%;background:var(--orange-light);color:var(--orange);display:flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0;">R</div>
            <div style="padding:8px 14px;border-radius:10px;border-top-left-radius:2px;background:var(--bg-alt);color:var(--text-muted);font-size:14px;">
              <strong>Xin chào!</strong> Tôi có thể giúp bạn:<br>
              • Twitter, web, papers<br>
              • Tính toán, tìm nhạc, tìm truyện<br>
              <span style="font-size:12px;color:var(--text-faint);">Thử: "120 X 5", "Tin AI hôm nay", "Tìm nhạc"</span>
            </div>
          </div>
        </div>
        <div style="display:flex;border-top:1px solid var(--border);padding:10px 16px;gap:8px;">
          <input type="text" id="chatInput" placeholder="Type a message..." style="flex:1;padding:10px 14px;border:1px solid var(--border);border-radius:var(--radius);font-size:14px;outline:none;background:#fff;font-family:inherit;">
          <button id="chatSendBtn" style="padding:10px 18px;background:var(--accent);color:#fff;border:none;border-radius:var(--radius);cursor:pointer;font-size:14px;transition:background 0.2s;">Send</button>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Footer -->
<footer>
  <span class="copy">© <?= $year ?> Research Agent. Open-source toolkit.</span>
  <div class="links">
    <a href="https://github.com/your-org/research-agent">GitHub</a>
    <a href="#demo">Demo</a>
  </div>
</footer>

<script>
// ── Scroll Reveal ──
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── CLI stagger ──
document.querySelectorAll('.cli-line').forEach((line, i) => {
  setTimeout(() => line.classList.add('visible'), 400 + i * 250);
});

// ── 3D Orbit Carousel (cylindrical, CSS transition smoothed) ──
(function() {
  const stage = document.getElementById('carouselStage');
  const slides = stage.querySelectorAll('.hero-3d-slide');
  const dots = document.querySelectorAll('.hero-3d-dots span');
  const N = slides.length;

  let currentIndex = 0;
  const autoInterval = 4000;
  let autoTimer = null;

  const radiusY = 40;
  const radiusZ = 250;

  function render3DOrbit() {
    const theta = (2 * Math.PI) / N;

    slides.forEach((slide, i) => {
      const angle = (i - currentIndex) * theta;

      const yVal = Math.sin(angle) * radiusY;
      const zVal = (Math.cos(angle) - 1) * radiusZ;

      const proximity = (Math.cos(angle) + 1) / 2;
      const scale = 0.85 + 0.15 * proximity;
      const opacity = 0.2 + 0.8 * proximity;

      slide.style.transform = `translate3d(0, ${yVal}px, ${zVal}px) scale(${scale})`;
      slide.style.opacity = opacity;
      slide.style.zIndex = Math.round(100 + (Math.cos(angle) * 100));

      slide.style.pointerEvents = Math.abs(angle) < 0.1 || Math.abs(angle - 2 * Math.PI) < 0.1
        ? 'auto' : 'none';
    });

    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === ((currentIndex % N) + N) % N);
    });
  }

  function nextSlide() {
    currentIndex++;
    render3DOrbit();
  }

  function startAutoplay() {
    stopAutoplay();
    autoTimer = setInterval(nextSlide, autoInterval);
  }

  function stopAutoplay() {
    if (autoTimer) clearInterval(autoTimer);
  }

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      const targetPos = i;
      const currentPos = (currentIndex % N + N) % N;
      let diff = targetPos - currentPos;
      if (diff > N / 2) diff -= N;
      if (diff < -N / 2) diff += N;
      currentIndex += diff;
      render3DOrbit();
      startAutoplay();
    });
  });

  stage.addEventListener('mouseenter', stopAutoplay);
  stage.addEventListener('mouseleave', startAutoplay);

  render3DOrbit();
  startAutoplay();
})();

// ── Nav scrolled state (IntersectionObserver, no scroll listener) ──
const nav = document.getElementById('nav');
const sentinel = document.createElement('div');
sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:1px;pointer-events:none;';
document.getElementById('hero').prepend(sentinel);
new IntersectionObserver(([e]) => nav.classList.toggle('scrolled', !e.isIntersecting), { threshold: 0 }).observe(sentinel);

// ── Chat ──
const chatInput = document.getElementById('chatInput');
const chatSend = document.getElementById('chatSendBtn');
const chatMsgs = document.getElementById('chatMessages');

function esc(t) { const d = document.createElement('div'); d.textContent = t; return d.innerHTML; }

function addChatMsg(role, html) {
  const div = document.createElement('div');
  div.style.cssText = 'display:flex;gap:8px;align-items:flex-start;animation:fadeUp 0.3s ease both;';
  const av = document.createElement('div');
  av.style.cssText = 'width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0;' +
    (role === 'user'
      ? 'background:var(--border);color:var(--text-muted);'
      : 'background:var(--orange-light);color:var(--orange);');
  av.textContent = role === 'user' ? 'U' : 'R';
  const b = document.createElement('div');
  b.style.cssText = 'padding:8px 14px;border-radius:10px;font-size:14px;line-height:1.6;' +
    (role === 'user'
      ? 'background:var(--bg-alt);color:var(--text);border-top-right-radius:2px;'
      : 'background:var(--bg-alt);color:var(--text-muted);border-top-left-radius:2px;');
  b.innerHTML = html;
  div.appendChild(av); div.appendChild(b);
  chatMsgs.appendChild(div);
  chatMsgs.scrollTop = chatMsgs.scrollHeight;
}

async function sendChat() {
  const text = chatInput.value.trim();
  if (!text) return;
  addChatMsg('user', esc(text));
  chatInput.value = '';
  chatSend.disabled = true;
  chatSend.textContent = '...';

  try {
    const res = await fetch('api.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    const botText = data.response || data.assistant_text || '(no response)';
    addChatMsg('bot', botText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>'));
    if (data.tool_calls?.length) {
      let info = '<div style="font-size:12px;color:var(--text-faint);margin-top:4px;">Tools: ';
      info += data.tool_calls.map(t => `<code style="background:rgba(0,0,0,0.04);padding:1px 6px;border-radius:4px;font-size:12px;">${esc(t.name)}</code>`).join(' ');
      info += '</div>';
      addChatMsg('bot', info);
    }
  } catch (err) {
    addChatMsg('bot', 'Connection error');
  }
  chatSend.disabled = false;
  chatSend.textContent = 'Send';
}

chatSend.addEventListener('click', sendChat);
chatInput.addEventListener('keydown', e => { if (e.key === 'Enter') sendChat(); });
</script>
</body>
</html>
