<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Smart AI Tour Planner — README</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0a0f1e;
    --surface: #111827;
    --surface2: #1a2235;
    --border: #1f3050;
    --accent: #3b82f6;
    --accent2: #06b6d4;
    --accent3: #8b5cf6;
    --green: #10b981;
    --yellow: #f59e0b;
    --red: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
    --faint: #1e2d42;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.75;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* ── Background grid ── */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(59,130,246,.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(59,130,246,.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* ── Glowing blobs ── */
  .blob {
    position: fixed;
    border-radius: 50%;
    filter: blur(120px);
    opacity: .18;
    pointer-events: none;
    z-index: 0;
  }
  .blob-1 { width: 600px; height: 600px; background: var(--accent3); top: -200px; left: -200px; }
  .blob-2 { width: 500px; height: 500px; background: var(--accent); bottom: -150px; right: -150px; }
  .blob-3 { width: 350px; height: 350px; background: var(--accent2); top: 40%; left: 50%; transform: translate(-50%,-50%); }

  /* ── Layout ── */
  .wrap {
    position: relative;
    z-index: 1;
    max-width: 860px;
    margin: 0 auto;
    padding: 60px 32px 100px;
  }

  /* ── HERO ── */
  .hero {
    text-align: center;
    padding: 70px 0 60px;
    animation: fadeUp .7s ease both;
  }

  .hero-icon {
    font-size: 56px;
    display: inline-block;
    margin-bottom: 18px;
    animation: float 4s ease-in-out infinite;
  }

  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
  }

  .hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 3.8rem);
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
    background: linear-gradient(135deg, #e2e8f0 30%, var(--accent2) 70%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 18px;
  }

  .hero p {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 560px;
    margin: 0 auto 30px;
    font-weight: 300;
  }

  .badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 12px;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
    letter-spacing: .5px;
    border: 1px solid;
  }
  .badge-blue   { background: rgba(59,130,246,.12);  border-color: rgba(59,130,246,.35);  color: #93c5fd; }
  .badge-cyan   { background: rgba(6,182,212,.12);   border-color: rgba(6,182,212,.35);   color: #67e8f9; }
  .badge-violet { background: rgba(139,92,246,.12);  border-color: rgba(139,92,246,.35);  color: #c4b5fd; }
  .badge-green  { background: rgba(16,185,129,.12);  border-color: rgba(16,185,129,.35);  color: #6ee7b7; }

  /* ── Divider ── */
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 48px 0;
  }

  /* ── Section heading ── */
  h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 10px;
    animation: fadeUp .5s ease both;
  }

  h2 .icon { font-size: 1.2rem; }

  h2::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 10px;
  }

  h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: var(--accent2);
    margin: 22px 0 10px;
    letter-spacing: .3px;
  }

  /* ── Cards ── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 26px;
    margin-bottom: 14px;
    transition: border-color .25s, transform .25s;
    animation: fadeUp .5s ease both;
  }

  .card:hover {
    border-color: rgba(59,130,246,.4);
    transform: translateY(-2px);
  }

  /* ── Feature grid ── */
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 14px;
    margin-bottom: 14px;
  }

  .feature-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    transition: border-color .25s, transform .25s, background .25s;
    animation: fadeUp .5s ease both;
  }

  .feature-card:hover {
    background: var(--surface2);
    border-color: rgba(59,130,246,.45);
    transform: translateY(-3px);
  }

  .feat-icon { font-size: 1.6rem; margin-bottom: 10px; display: block; }
  .feat-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: .9rem; margin-bottom: 6px; color: #f1f5f9; }
  .feat-desc  { font-size: .84rem; color: var(--muted); line-height: 1.55; }

  /* ── Tech table ── */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: .88rem;
    margin-bottom: 6px;
  }

  thead th {
    font-family: 'DM Mono', monospace;
    font-size: .75rem;
    letter-spacing: .8px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 10px 16px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }

  tbody tr {
    border-bottom: 1px solid rgba(31,48,80,.5);
    transition: background .2s;
  }

  tbody tr:hover { background: rgba(59,130,246,.06); }

  tbody td {
    padding: 10px 16px;
    color: var(--text);
  }

  tbody td:first-child { color: var(--muted); font-family: 'DM Mono', monospace; font-size: .8rem; }

  tbody td a {
    color: var(--accent2);
    text-decoration: none;
    border-bottom: 1px solid rgba(6,182,212,.3);
    transition: border-color .2s;
  }

  tbody td a:hover { border-color: var(--accent2); }

  /* ── Steps ── */
  .steps { counter-reset: step; display: flex; flex-direction: column; gap: 12px; }

  .step {
    display: flex;
    gap: 18px;
    align-items: flex-start;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 22px;
    transition: border-color .2s, transform .2s;
    animation: fadeUp .5s ease both;
  }

  .step:hover { border-color: rgba(59,130,246,.4); transform: translateX(4px); }

  .step-num {
    counter-increment: step;
    content: counter(step);
    min-width: 34px;
    height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent3));
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: .85rem;
    color: #fff;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .step-body h3 { margin: 0 0 4px; color: #f1f5f9; font-size: .95rem; }
  .step-body p  { margin: 0; font-size: .88rem; color: var(--muted); }

  /* ── Code blocks ── */
  pre {
    background: #0d1626;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 22px;
    overflow-x: auto;
    font-family: 'DM Mono', monospace;
    font-size: .8rem;
    line-height: 1.7;
    color: #94a3b8;
    margin: 14px 0;
    position: relative;
  }

  pre .kw  { color: #c4b5fd; }
  pre .fn  { color: #67e8f9; }
  pre .str { color: #6ee7b7; }
  pre .cm  { color: #475569; font-style: italic; }
  pre .hl  { color: #f1f5f9; }

  code:not(pre code) {
    background: rgba(59,130,246,.12);
    color: #93c5fd;
    font-family: 'DM Mono', monospace;
    font-size: .82em;
    padding: 2px 7px;
    border-radius: 5px;
    border: 1px solid rgba(59,130,246,.2);
  }

  /* ── Info / warning boxes ── */
  .info-box {
    border-radius: 10px;
    padding: 14px 18px;
    font-size: .88rem;
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin: 16px 0;
    line-height: 1.6;
  }

  .info-box.blue   { background: rgba(59,130,246,.1);  border: 1px solid rgba(59,130,246,.3);  color: #bfdbfe; }
  .info-box.yellow { background: rgba(245,158,11,.1);  border: 1px solid rgba(245,158,11,.3);  color: #fde68a; }
  .info-box.green  { background: rgba(16,185,129,.1);  border: 1px solid rgba(16,185,129,.3);  color: #a7f3d0; }

  .info-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }

  /* ── File tree ── */
  .tree {
    background: #0d1626;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 22px;
    font-family: 'DM Mono', monospace;
    font-size: .82rem;
    line-height: 2;
    color: #64748b;
  }

  .tree .file  { color: #94a3b8; }
  .tree .dir   { color: var(--accent2); font-weight: 500; }
  .tree .cmnt  { color: #475569; }

  /* ── Limitations list ── */
  .limit-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }

  .limit-list li {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 12px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-size: .88rem;
    color: var(--muted);
    line-height: 1.55;
  }

  .limit-list li::before {
    content: '⚠';
    color: var(--yellow);
    flex-shrink: 0;
    margin-top: 1px;
  }

  /* ── Footer ── */
  footer {
    text-align: center;
    margin-top: 80px;
    padding-top: 30px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: .82rem;
  }

  footer a { color: var(--accent2); text-decoration: none; }

  /* ── Section spacing ── */
  section { margin-bottom: 56px; }

  /* ── Animations ── */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .delay-1 { animation-delay: .1s; }
  .delay-2 { animation-delay: .2s; }
  .delay-3 { animation-delay: .3s; }
  .delay-4 { animation-delay: .4s; }

  p { color: #94a3b8; margin-bottom: 12px; }
</style>
</head>
<body>

<div class="blob blob-1"></div>
<div class="blob blob-2"></div>
<div class="blob blob-3"></div>

<div class="wrap">

  <!-- ══ HERO ══ -->
  <div class="hero">
    <div class="hero-icon">🌍</div>
    <h1>Smart AI Tour Planner</h1>
    <p>An agentic travel assistant that combines real-time weather, restaurant discovery, and multi-LLM power to craft personalized trip itineraries — all in your browser.</p>
    <div class="badge-row">
      <span class="badge badge-blue">🤖 Multi-LLM</span>
      <span class="badge badge-cyan">🌤 Live Weather</span>
      <span class="badge badge-violet">🍽 Restaurant Finder</span>
      <span class="badge badge-green">🔒 Session-only Keys</span>
    </div>
  </div>

  <div class="divider"></div>

  <!-- ══ FEATURES ══ -->
  <section>
    <h2><span class="icon">✨</span>Features</h2>
    <div class="feature-grid">
      <div class="feature-card delay-1">
        <span class="feat-icon">🤖</span>
        <div class="feat-title">Multi-LLM Support</div>
        <div class="feat-desc">Choose between Grok (xAI), GPT-4o, or Gemini 1.5 Pro from the sidebar.</div>
      </div>
      <div class="feature-card delay-2">
        <span class="feat-icon">🌤️</span>
        <div class="feat-title">Live Weather Forecasts</div>
        <div class="feat-desc">Fetches real-time weather for your destination via OpenWeatherMap API.</div>
      </div>
      <div class="feature-card delay-3">
        <span class="feat-icon">🍽️</span>
        <div class="feat-title">Restaurant Discovery</div>
        <div class="feat-desc">Finds top nearby restaurants using the Google Maps Places API.</div>
      </div>
      <div class="feature-card delay-4">
        <span class="feat-icon">🔄</span>
        <div class="feat-title">Agentic Tool Use</div>
        <div class="feat-desc">The LLM autonomously decides when to call weather and restaurant tools — up to 5 turns.</div>
      </div>
    </div>
  </section>

  <!-- ══ TECH STACK ══ -->
  <section>
    <h2><span class="icon">🛠</span>Tech Stack</h2>
    <div class="card">
      <table>
        <thead>
          <tr>
            <th>Component</th>
            <th>Technology</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>UI Framework</td><td><a href="https://streamlit.io">Streamlit</a></td></tr>
          <tr><td>LLM Orchestration</td><td><a href="https://github.com/andrewyng/aisuite">AISuite</a></td></tr>
          <tr><td>Weather Data</td><td><a href="https://openweathermap.org/api">OpenWeatherMap API</a></td></tr>
          <tr><td>Places Data</td><td><a href="https://developers.google.com/maps/documentation/places/web-service">Google Maps Places API</a></td></tr>
          <tr><td>Language Models</td><td>xAI Grok-2 · OpenAI GPT-4o · Google Gemini 1.5 Pro</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <!-- ══ PREREQUISITES ══ -->
  <section>
    <h2><span class="icon">📋</span>Prerequisites</h2>
    <div class="card">
      <p style="margin-bottom:14px;">You will need <strong style="color:#f1f5f9">Python 3.9+</strong> and API keys for the following services:</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">
        <li style="display:flex;gap:10px;align-items:center;font-size:.88rem;color:#94a3b8"><span style="color:#3b82f6">●</span> <a href="https://console.x.ai/" style="color:#67e8f9;text-decoration:none;border-bottom:1px solid rgba(6,182,212,.3)">xAI (Grok)</a> — or OpenAI / Google depending on your model choice</li>
        <li style="display:flex;gap:10px;align-items:center;font-size:.88rem;color:#94a3b8"><span style="color:#06b6d4">●</span> <a href="https://home.openweathermap.org/api_keys" style="color:#67e8f9;text-decoration:none;border-bottom:1px solid rgba(6,182,212,.3)">OpenWeatherMap</a> — free tier is sufficient</li>
        <li style="display:flex;gap:10px;align-items:center;font-size:.88rem;color:#94a3b8"><span style="color:#8b5cf6">●</span> <a href="https://console.cloud.google.com/" style="color:#67e8f9;text-decoration:none;border-bottom:1px solid rgba(6,182,212,.3)">Google Maps Platform</a> — with Places API enabled</li>
      </ul>
    </div>
  </section>

  <!-- ══ GETTING STARTED ══ -->
  <section>
    <h2><span class="icon">🚀</span>Getting Started</h2>
    <div class="steps">

      <div class="step">
        <div class="step-num">1</div>
        <div class="step-body">
          <h3>Clone the Repository</h3>
          <pre><span class="kw">git</span> clone https://github.com/your-username/smart-ai-tour-planner.git
<span class="kw">cd</span> smart-ai-tour-planner</pre>
        </div>
      </div>

      <div class="step">
        <div class="step-num">2</div>
        <div class="step-body">
          <h3>Install Dependencies</h3>
          <pre><span class="kw">pip</span> install -r requirements.txt</pre>
          <div class="info-box yellow" style="margin-top:12px">
            <span class="info-icon">⚠️</span>
            <span>AISuite requires provider-specific packages. Install based on your chosen model:<br>
            <code>pip install openai</code> · <code>pip install google-generativeai</code> · <code>pip install anthropic</code></span>
          </div>
        </div>
      </div>

      <div class="step">
        <div class="step-num">3</div>
        <div class="step-body">
          <h3>Run the App</h3>
          <pre><span class="kw">streamlit</span> run app.py</pre>
        </div>
      </div>

      <div class="step">
        <div class="step-num">4</div>
        <div class="step-body">
          <h3>Enter Your API Keys</h3>
          <p>In the <strong style="color:#f1f5f9">sidebar</strong>, enter your Grok, OpenWeatherMap, and Google Maps API keys — then type a destination and click <strong style="color:#f1f5f9">Plan My Trip</strong>!</p>
        </div>
      </div>

    </div>
  </section>

  <!-- ══ REQUIREMENTS ══ -->
  <section>
    <h2><span class="icon">📦</span>Requirements</h2>
    <p>Create a <code>requirements.txt</code> with:</p>
    <pre><span class="hl">streamlit
aisuite
requests</span></pre>
  </section>

  <!-- ══ PROJECT STRUCTURE ══ -->
  <section>
    <h2><span class="icon">📁</span>Project Structure</h2>
    <div class="tree">
      <span class="dir">smart-ai-tour-planner/</span><br>
      ├── <span class="file">app.py</span>              <span class="cmnt"># Main Streamlit application</span><br>
      ├── <span class="file">requirements.txt</span>    <span class="cmnt"># Python dependencies</span><br>
      └── <span class="file">README.md</span>           <span class="cmnt"># Project documentation</span>
    </div>
  </section>

  <!-- ══ HOW IT WORKS ══ -->
  <section>
    <h2><span class="icon">⚙️</span>How It Works</h2>
    <div class="card">
      <p>The app follows a simple <strong style="color:#f1f5f9">agentic loop</strong>:</p>
      <ol style="list-style:none;display:flex;flex-direction:column;gap:10px;margin-top:14px">
        <li style="display:flex;gap:12px;align-items:flex-start;font-size:.88rem;color:#94a3b8"><span style="color:#3b82f6;font-family:'DM Mono',monospace;font-size:.8rem;min-width:22px;margin-top:1px">01</span><span><strong style="color:#e2e8f0">User Input</strong> — Enter a destination and select an LLM model.</span></li>
        <li style="display:flex;gap:12px;align-items:flex-start;font-size:.88rem;color:#94a3b8"><span style="color:#06b6d4;font-family:'DM Mono',monospace;font-size:.8rem;min-width:22px;margin-top:1px">02</span><span><strong style="color:#e2e8f0">Agent Invocation</strong> — AISuite sends the request to the LLM with tool definitions.</span></li>
        <li style="display:flex;gap:12px;align-items:flex-start;font-size:.88rem;color:#94a3b8"><span style="color:#8b5cf6;font-family:'DM Mono',monospace;font-size:.8rem;min-width:22px;margin-top:1px">03</span><span><strong style="color:#e2e8f0">Tool Calls</strong> — The LLM autonomously decides when to call <code>get_weather</code> and <code>find_restaurants</code>.</span></li>
        <li style="display:flex;gap:12px;align-items:flex-start;font-size:.88rem;color:#94a3b8"><span style="color:#10b981;font-family:'DM Mono',monospace;font-size:.8rem;min-width:22px;margin-top:1px">04</span><span><strong style="color:#e2e8f0">Data Fetching</strong> — Tools hit the OpenWeatherMap and Google Maps APIs in real time.</span></li>
        <li style="display:flex;gap:12px;align-items:flex-start;font-size:.88rem;color:#94a3b8"><span style="color:#f59e0b;font-family:'DM Mono',monospace;font-size:.8rem;min-width:22px;margin-top:1px">05</span><span><strong style="color:#e2e8f0">Plan Generation</strong> — The LLM synthesizes all data into a complete, readable itinerary.</span></li>
      </ol>
    </div>
  </section>

  <!-- ══ EXTENDING ══ -->
  <section>
    <h2><span class="icon">🧩</span>Extending the App</h2>
    <p>Add more tools by defining new Python functions and passing them in the <code>tools</code> list:</p>
    <pre><span class="kw">def</span> <span class="fn">find_hotels</span>(location: <span class="hl">str</span>):
    <span class="cm"># Call a hotels API here</span>
    ...

response = client.chat.completions.<span class="fn">create</span>(
    model=selected_model,
    messages=messages,
    tools=[get_weather, find_restaurants, <span class="hl">find_hotels</span>],  <span class="cm"># Add here</span>
    max_turns=<span class="str">5</span>
)</pre>
  </section>

  <!-- ══ SECURITY ══ -->
  <section>
    <h2><span class="icon">🔒</span>Privacy &amp; Security</h2>
    <div class="info-box green">
      <span class="info-icon">🛡️</span>
      <div>
        API keys are passed as <code>type="password"</code> inputs — masked in the UI, stored only in <code>os.environ</code> for the duration of the session, and <strong>never persisted</strong> to disk or any external service. No trip plans or user data are logged.
      </div>
    </div>
  </section>

  <!-- ══ LIMITATIONS ══ -->
  <section>
    <h2><span class="icon">⚠️</span>Known Limitations</h2>
    <ul class="limit-list">
      <li>Weather forecast is simplified to the first 3 time slots from the 5-day OpenWeatherMap endpoint.</li>
      <li>Restaurant results are limited to the top 3 from the Google Places text search query.</li>
      <li>Mismatched API keys and model selection will cause runtime errors — ensure keys match your chosen model.</li>
    </ul>
  </section>

  <!-- ══ LICENSE ══ -->
  <section>
    <h2><span class="icon">📄</span>License</h2>
    <div class="card" style="font-size:.88rem;color:#64748b">
      This project is licensed under the <strong style="color:#f1f5f9">MIT License</strong>. See the <code>LICENSE</code> file for full details.
    </div>
  </section>

  <!-- ══ ACKNOWLEDGEMENTS ══ -->
  <section>
    <h2><span class="icon">🙏</span>Acknowledgements</h2>
    <div style="display:flex;flex-direction:column;gap:10px">
      <div class="card" style="display:flex;gap:14px;align-items:center">
        <span style="font-size:1.4rem">🧠</span>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.9rem;margin-bottom:3px;color:#f1f5f9">AISuite by Andrew Ng</div>
          <div style="font-size:.83rem;color:#64748b">Unified LLM interface that powers multi-model support.</div>
        </div>
      </div>
      <div class="card" style="display:flex;gap:14px;align-items:center">
        <span style="font-size:1.4rem">🎈</span>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.9rem;margin-bottom:3px;color:#f1f5f9">Streamlit</div>
          <div style="font-size:.83rem;color:#64748b">Making Python web apps effortlessly beautiful.</div>
        </div>
      </div>
      <div class="card" style="display:flex;gap:14px;align-items:center">
        <span style="font-size:1.4rem">🗺️</span>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.9rem;margin-bottom:3px;color:#f1f5f9">OpenWeatherMap &amp; Google Maps Platform</div>
          <div style="font-size:.83rem;color:#64748b">Real-time data APIs that make the travel plans genuinely useful.</div>
        </div>
      </div>
    </div>
  </section>

  <div class="divider"></div>

  <footer>
    <p>Built with ❤️ using <a href="https://streamlit.io">Streamlit</a> · <a href="https://github.com/andrewyng/aisuite">AISuite</a> · <a href="https://openweathermap.org">OpenWeatherMap</a> · <a href="https://developers.google.com/maps">Google Maps</a></p>
    <p style="margin-top:6px">MIT License · Smart AI Tour Planner</p>
  </footer>

</div>
</body>
</html>
