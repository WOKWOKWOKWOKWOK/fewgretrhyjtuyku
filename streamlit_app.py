import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Utopia Education",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide default Streamlit chrome (header, footer, toolbar, padding) and stretch
# the HTML component iframe to fill 100vw x 100vh seamlessly.
st.markdown(
    """
    <style>
        #MainMenu,
        header,
        footer,
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
        }

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .main,
        .block-container,
        [data-testid="stMainBlockContainer"],
        [data-testid="stVerticalBlock"],
        [data-testid="stElementContainer"],
        .element-container {
            margin: 0 !important;
            padding: 0 !important;
            width: 100vw !important;
            max-width: 100vw !important;
            height: 100vh !important;
            max-height: 100vh !important;
            overflow: hidden !important;
            background-color: #0f172a !important;
        }

        iframe,
        [data-testid="stCustomComponentV1"] iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            margin: 0 !important;
            padding: 0 !important;
            display: block !important;
            z-index: 999999 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_APP = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Utopia Education</title>
  <style>
    :root {
      --bg-primary: #0f172a;
      --bg-secondary: #1e293b;
      --bg-tertiary: #273549;
      --border-subtle: rgba(148, 163, 184, 0.14);
      --border-strong: rgba(148, 163, 184, 0.28);
      --accent: #6366f1;
      --accent-hover: #4f46e5;
      --accent-soft: rgba(99, 102, 241, 0.16);
      --accent-glow: rgba(99, 102, 241, 0.32);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --success: #10b981;
      --warning: #f59e0b;
      --radius-lg: 16px;
      --radius-md: 10px;
      --radius-sm: 8px;
      --transition: 160ms cubic-bezier(0.22, 1, 0.36, 1);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    html,
    body {
      width: 100%;
      height: 100%;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Subtle ambient background glow */
    .ambient-bg {
      position: fixed;
      inset: 0;
      pointer-events: none;
      background:
        radial-gradient(circle at 20% 15%, rgba(99, 102, 241, 0.14) 0%, transparent 45%),
        radial-gradient(circle at 82% 85%, rgba(56, 189, 248, 0.08) 0%, transparent 45%);
      z-index: 0;
    }

    /* View Containers */
    .view {
      position: relative;
      z-index: 1;
      width: 100%;
      height: 100%;
      display: none;
      flex-direction: column;
    }

    .view.active {
      display: flex;
    }

    /* Shared Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      border: 1px solid var(--border-subtle);
      background: var(--bg-secondary);
      color: var(--text-primary);
      font-size: 13px;
      font-weight: 500;
      padding: 7px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
      text-decoration: none;
      white-space: nowrap;
      user-select: none;
    }

    .btn:hover:not(:disabled) {
      background: var(--bg-tertiary);
      border-color: var(--border-strong);
    }

    .btn:active:not(:disabled) {
      transform: translateY(1px);
    }

    .btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    .btn-accent {
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
    }

    .btn-accent:hover:not(:disabled) {
      background: var(--accent-hover);
      border-color: var(--accent-hover);
      box-shadow: 0 4px 16px var(--accent-glow);
    }

    .btn-icon {
      padding: 7px;
      width: 32px;
      height: 32px;
    }

    .kbd-hint {
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 5px;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    /* ================= HOME DASHBOARD ================= */
    #view-home {
      overflow-y: auto;
      padding: 20px 28px 32px;
    }

    .home-topbar {
      width: 100%;
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .brand-pill {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-weight: 600;
      font-size: 15px;
      color: var(--text-primary);
    }

    .brand-logo {
      width: 32px;
      height: 32px;
      border-radius: 9px;
      background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
      display: grid;
      place-items: center;
      box-shadow: 0 4px 14px var(--accent-glow);
    }

    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      color: var(--text-secondary);
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid var(--border-subtle);
      padding: 5px 11px;
      border-radius: 999px;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 8px rgba(16, 185, 129, 0.7);
    }

    .home-main {
      width: 100%;
      max-width: 1140px;
      margin: auto;
      padding-top: 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .hero-title {
      font-size: clamp(28px, 4vw, 40px);
      font-weight: 700;
      letter-spacing: -0.025em;
      text-align: center;
      margin-bottom: 8px;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
      font-size: 15px;
      color: var(--text-secondary);
      text-align: center;
      max-width: 580px;
      line-height: 1.5;
      margin-bottom: 24px;
    }

    /* Centered Search / URL Bar */
    .search-wrapper {
      width: 100%;
      max-width: 680px;
      margin-bottom: 14px;
    }

    .search-box {
      display: flex;
      align-items: center;
      background: var(--bg-secondary);
      border: 1px solid var(--border-strong);
      border-radius: 14px;
      padding: 6px 8px 6px 16px;
      gap: 10px;
      box-shadow: 0 12px 32px rgba(2, 6, 23, 0.45);
      transition: border-color var(--transition), box-shadow var(--transition);
    }

    .search-box:focus-within {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px var(--accent-soft), 0 14px 36px rgba(2, 6, 23, 0.55);
    }

    .search-box input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-primary);
      font-size: 15px;
      min-width: 0;
    }

    .search-box input::placeholder {
      color: var(--text-muted);
    }

    .quick-chips {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 8px;
      margin-bottom: 30px;
    }

    .chip {
      font-size: 12px;
      color: var(--text-secondary);
      background: rgba(30, 41, 59, 0.75);
      border: 1px solid var(--border-subtle);
      padding: 5px 12px;
      border-radius: 999px;
      cursor: pointer;
      transition: all var(--transition);
    }

    .chip:hover {
      color: var(--text-primary);
      border-color: var(--accent);
      background: var(--accent-soft);
    }

    /* Subject Quick-Launch Cards Grid */
    .section-label {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      margin-bottom: 12px;
    }

    .cards-grid {
      width: 100%;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }

    @media (max-width: 900px) {
      .cards-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 600px) {
      .cards-grid {
        grid-template-columns: 1fr;
      }
    }

    .subject-card {
      background: rgba(30, 41, 59, 0.82);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 14px;
      cursor: pointer;
      transition: transform var(--transition), border-color var(--transition), background var(--transition), box-shadow var(--transition);
    }

    .subject-card:hover {
      transform: translateY(-2px);
      background: var(--bg-secondary);
      border-color: rgba(99, 102, 241, 0.55);
      box-shadow: 0 12px 28px rgba(2, 6, 23, 0.45);
    }

    .card-top {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
    }

    .card-icon {
      width: 40px;
      height: 40px;
      border-radius: 11px;
      background: var(--accent-soft);
      border: 1px solid rgba(99, 102, 241, 0.28);
      color: #818cf8;
      display: grid;
      place-items: center;
      flex-shrink: 0;
    }

    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 4px;
    }

    .card-desc {
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.45;
    }

    .card-links {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding-top: 4px;
      border-top: 1px solid var(--border-subtle);
    }

    .resource-pill {
      font-size: 11.5px;
      font-weight: 500;
      color: #c7d2fe;
      background: rgba(99, 102, 241, 0.14);
      border: 1px solid rgba(99, 102, 241, 0.24);
      padding: 4px 9px;
      border-radius: 6px;
      cursor: pointer;
      transition: background var(--transition), border-color var(--transition);
    }

    .resource-pill:hover {
      background: var(--accent);
      border-color: var(--accent);
      color: #ffffff;
    }

    /* ================= EMBEDDED WEB VIEWER ================= */
    .viewer-navbar {
      height: 50px;
      min-height: 50px;
      background: var(--bg-primary);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      position: relative;
      z-index: 10;
    }

    .url-bar-form {
      flex: 1;
      display: flex;
      align-items: center;
      background: var(--bg-secondary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 0 10px;
      height: 34px;
      gap: 8px;
      min-width: 0;
      transition: border-color var(--transition);
    }

    .url-bar-form:focus-within {
      border-color: var(--accent);
    }

    .url-bar-form input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text-primary);
      font-size: 13px;
      min-width: 0;
    }

    .shield-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      color: #34d399;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.25);
      padding: 3px 8px;
      border-radius: 999px;
      white-space: nowrap;
    }

    @media (max-width: 860px) {
      .shield-pill,
      .hide-mobile {
        display: none;
      }
    }

    /* Thin loading bar under navbar */
    .load-bar {
      position: absolute;
      left: 0;
      bottom: -1px;
      height: 2px;
      width: 0%;
      background: linear-gradient(90deg, #6366f1, #38bdf8);
      transition: width 260ms ease, opacity 200ms ease;
      opacity: 0;
    }

    .load-bar.loading {
      opacity: 1;
      width: 85%;
    }

    .load-bar.done {
      opacity: 0;
      width: 100%;
    }

    /* X-Frame-Options Fallback Notice Banner */
    .fallback-banner {
      background: rgba(30, 41, 59, 0.96);
      border-bottom: 1px solid rgba(245, 158, 11, 0.35);
      padding: 9px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 13px;
      color: var(--text-primary);
    }

    .fallback-banner.compact {
      background: rgba(15, 23, 42, 0.94);
      border-bottom: 1px solid var(--border-subtle);
      padding: 6px 16px;
      font-size: 12px;
      color: var(--text-secondary);
    }

    .fallback-text {
      display: flex;
      align-items: center;
      gap: 8px;
      line-height: 1.4;
    }

    .fallback-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }

    .iframe-stage {
      flex: 1;
      width: 100%;
      height: 100%;
      position: relative;
      background: #ffffff;
    }

    #web-frame {
      width: 100%;
      height: 100%;
      border: none;
      display: block;
      background: #ffffff;
    }

    /* ================= FOCUS MODE (STUDY NOTES + WIKIPEDIA SUMMARY) ================= */
    #view-focus {
      background: var(--bg-primary);
    }

    .focus-header {
      height: 52px;
      min-height: 52px;
      padding: 0 20px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: rgba(15, 23, 42, 0.95);
    }

    .focus-title-group {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .focus-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 12px;
      font-weight: 600;
      color: #c7d2fe;
      background: var(--accent-soft);
      border: 1px solid rgba(99, 102, 241, 0.35);
      padding: 4px 10px;
      border-radius: 999px;
    }

    .focus-workspace {
      flex: 1;
      width: 100%;
      max-width: 1280px;
      margin: 0 auto;
      padding: 20px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      overflow: hidden;
    }

    @media (max-width: 840px) {
      .focus-workspace {
        grid-template-columns: 1fr;
        overflow-y: auto;
      }
    }

    .focus-panel {
      background: var(--bg-secondary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      min-height: 300px;
    }

    .panel-header {
      padding: 14px 16px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .panel-header h2 {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .wiki-search-bar {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      gap: 8px;
    }

    .wiki-search-bar input {
      flex: 1;
      background: var(--bg-primary);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 8px 12px;
      color: var(--text-primary);
      font-size: 13px;
      outline: none;
    }

    .wiki-search-bar input:focus {
      border-color: var(--accent);
    }

    .wiki-content {
      flex: 1;
      padding: 18px;
      overflow-y: auto;
      line-height: 1.65;
      font-size: 14px;
      color: #e2e8f0;
    }

    .wiki-article-title {
      font-size: 20px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }

    .wiki-article-desc {
      font-size: 12.5px;
      color: #818cf8;
      margin-bottom: 14px;
      font-weight: 500;
    }

    .wiki-article-body {
      color: #cbd5e1;
      margin-bottom: 16px;
    }

    .notes-textarea {
      flex: 1;
      width: 100%;
      background: transparent;
      border: none;
      outline: none;
      resize: none;
      padding: 16px;
      color: var(--text-primary);
      font-family: inherit;
      font-size: 14px;
      line-height: 1.7;
    }

    .notes-textarea::placeholder {
      color: var(--text-muted);
    }

    .panel-footer {
      padding: 10px 16px;
      border-top: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-muted);
      background: rgba(15, 23, 42, 0.35);
    }
  </style>
</head>
<body>
  <div class="ambient-bg"></div>

  <!-- ==================== 1. HOME DASHBOARD ==================== -->
  <section id="view-home" class="view active">
    <header class="home-topbar">
      <div class="brand-pill">
        <div class="brand-logo" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
            <path d="M6 12v5c3 3 9 3 12 0v-5"/>
          </svg>
        </div>
        <span>Utopia Education</span>
      </div>

      <div style="display:flex; align-items:center; gap:10px;">
        <div class="status-badge">
          <span class="status-dot"></span>
          <span>Popup Blocker Active</span>
        </div>
        <button class="btn" onclick="toggleFocusMode()" title="Switch to Focus Mode (Esc)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
          <span>Focus Mode</span>
          <span class="kbd-hint">Esc</span>
        </button>
      </div>
    </header>

    <main class="home-main">
      <h1 class="hero-title">Utopia Education</h1>
      <p class="hero-subtitle">
        Your all-in-one distraction-free educational resource hub, sandboxed web viewer, and instant study notes workspace.
      </p>

      <form class="search-wrapper" onsubmit="handleHomeSearch(event)">
        <div class="search-box">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
          </svg>
          <input
            id="home-search-input"
            type="text"
            placeholder="Enter an educational URL (e.g., desmos.com/calculator) or search any topic..."
            autocomplete="off"
          />
          <button type="submit" class="btn btn-accent" style="padding: 9px 18px; border-radius: 10px;">
            Open
          </button>
        </div>
      </form>

      <div class="quick-chips">
        <button class="chip" onclick="openResource('https://en.wikipedia.org/wiki/Main_Page')">Wikipedia</button>
        <button class="chip" onclick="openResource('https://www.desmos.com/calculator')">Desmos Graphing</button>
        <button class="chip" onclick="openResource('https://phet.colorado.edu/en/simulations/filter')">PhET Simulations</button>
        <button class="chip" onclick="openResource('https://www.khanacademy.org')">Khan Academy</button>
        <button class="chip" onclick="openResource('https://www.gutenberg.org')">Project Gutenberg</button>
        <button class="chip" onclick="openResource('https://mathworld.wolfram.com')">Wolfram MathWorld</button>
      </div>

      <div class="section-label">
        <span>Subject Quick-Launch</span>
        <span>Click any card or resource pill to launch</span>
      </div>

      <div class="cards-grid">
        <!-- Math -->
        <div class="subject-card" onclick="openResource('https://www.desmos.com/calculator')">
          <div class="card-top">
            <div>
              <div class="card-title">Math</div>
              <div class="card-desc">Interactive graphing calculators, algebra, calculus, and step-by-step problem solving.</div>
            </div>
            <div class="card-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/><line x1="8" y1="6" x2="8" y2="10"/><line x1="6" y1="8" x2="10" y2="8"/><line x1="14" y1="16" x2="18" y2="16"/>
              </svg>
            </div>
          </div>
          <div class="card-links">
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.desmos.com/calculator')">Desmos</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Portal:Mathematics')">Wikipedia Math</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.khanacademy.org/math')">Khan Academy</span>
          </div>
        </div>

        <!-- Science -->
        <div class="subject-card" onclick="openResource('https://phet.colorado.edu/en/simulations/filter')">
          <div class="card-top">
            <div>
              <div class="card-title">Science</div>
              <div class="card-desc">Physics, chemistry, and biology simulations alongside peer-reviewed reference guides.</div>
            </div>
            <div class="card-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 3h6"/><path d="M10 9h4"/><path d="M10 3v6l-4 11a1 1 0 0 0 .9 1.4h10.2a1 1 0 0 0 .9-1.4L14 9V3"/>
              </svg>
            </div>
          </div>
          <div class="card-links">
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://phet.colorado.edu/en/simulations/filter')">PhET Labs</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Portal:Science')">Wikipedia Science</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.khanacademy.org/science')">Khan Academy</span>
          </div>
        </div>

        <!-- History -->
        <div class="subject-card" onclick="openResource('https://en.wikipedia.org/wiki/Portal:History')">
          <div class="card-top">
            <div>
              <div class="card-title">History</div>
              <div class="card-desc">World civilizations, primary historical archives, timelines, and modern era studies.</div>
            </div>
            <div class="card-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
          </div>
          <div class="card-links">
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Portal:History')">Wikipedia History</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.khanacademy.org/humanities/world-history')">Khan History</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.loc.gov')">Library of Congress</span>
          </div>
        </div>

        <!-- Literature -->
        <div class="subject-card" onclick="openResource('https://www.gutenberg.org')">
          <div class="card-top">
            <div>
              <div class="card-title">Literature</div>
              <div class="card-desc">Classic novels, poetry anthologies, literary analysis, and open-access eBooks.</div>
            </div>
            <div class="card-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
              </svg>
            </div>
          </div>
          <div class="card-links">
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.gutenberg.org')">Project Gutenberg</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Portal:Literature')">Wikipedia Literature</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://standardebooks.org')">Standard Ebooks</span>
          </div>
        </div>

        <!-- Social Studies -->
        <div class="subject-card" onclick="openResource('https://en.wikipedia.org/wiki/Portal:Society')">
          <div class="card-top">
            <div>
              <div class="card-title">Social Studies</div>
              <div class="card-desc">Civics, economics, human geography, sociology, and global cultural perspectives.</div>
            </div>
            <div class="card-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
              </svg>
            </div>
          </div>
          <div class="card-links">
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Portal:Society')">Society Portal</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://www.khanacademy.org/economics-finance-domain')">Khan Economics</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Geography')">Geography</span>
          </div>
        </div>

        <!-- Writing -->
        <div class="subject-card" onclick="openResource('https://en.wikipedia.org/wiki/Academic_writing')">
          <div class="card-top">
            <div>
              <div class="card-title">Writing</div>
              <div class="card-desc">Essay structure, rhetoric, grammar guides, citations, and vocabulary dictionaries.</div>
            </div>
            <div class="card-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>
              </svg>
            </div>
          </div>
          <div class="card-links">
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wikipedia.org/wiki/Academic_writing')">Academic Writing</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://en.wiktionary.org/wiki/Wiktionary:Main_Page')">Wiktionary</span>
            <span class="resource-pill" onclick="event.stopPropagation(); openResource('https://owl.purdue.edu/owl/')">Purdue OWL</span>
          </div>
        </div>
      </div>
    </main>
  </section>

  <!-- ==================== 2. EMBEDDED WEB VIEWER ==================== -->
  <section id="view-viewer" class="view">
    <nav class="viewer-navbar">
      <button class="btn btn-icon" onclick="showHome()" title="Home Dashboard">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>
        </svg>
      </button>

      <button id="btn-back" class="btn btn-icon" onclick="goBack()" title="Back" disabled>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m15 18-6-6 6-6"/>
        </svg>
      </button>

      <button class="btn btn-icon" onclick="reloadFrame()" title="Reload Page">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>
        </svg>
      </button>

      <form class="url-bar-form" onsubmit="handleNavbarSubmit(event)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
        <input
          id="viewer-url-input"
          type="text"
          placeholder="Enter URL or search topic..."
          onfocus="this.select()"
          autocomplete="off"
        />
      </form>

      <span class="shield-pill" title="Iframe sandboxed with allow-scripts allow-same-origin allow-forms to block popups automatically">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>
        </svg>
        Popups Blocked
      </span>

      <a id="nav-new-tab" class="btn" href="https://en.wikipedia.org" target="_blank" rel="noopener noreferrer" title="Open current page in a new browser tab">
        <span class="hide-mobile">New Tab</span>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>
        </svg>
      </a>

      <button class="btn btn-accent" onclick="toggleFocusMode()" title="Focus Mode: Study Notes & Wikipedia Summary (Esc)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
        </svg>
        <span class="hide-mobile">Focus Mode</span>
        <span class="kbd-hint" style="background:rgba(15,23,42,0.45); color:#fff; border-color:rgba(255,255,255,0.2);">Esc</span>
      </button>

      <button class="btn btn-icon" onclick="toggleFullscreen()" title="Toggle Fullscreen">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/>
        </svg>
      </button>

      <div id="load-bar" class="load-bar"></div>
    </nav>

    <!-- X-Frame-Options Fallback Notice -->
    <div id="fallback-banner" class="fallback-banner">
      <div class="fallback-text">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span id="fallback-message">
          Some websites restrict iframe embedding via <strong>X-Frame-Options</strong> headers. If the frame below appears blank or refuses to connect, open it directly in a new tab.
        </span>
      </div>
      <div class="fallback-actions">
        <a id="fallback-new-tab" class="btn btn-accent" href="https://en.wikipedia.org" target="_blank" rel="noopener noreferrer" style="padding: 5px 12px; font-size: 12px;">
          Open in New Tab ↗
        </a>
        <button id="fallback-dismiss" class="btn btn-icon" onclick="collapseFallbackBanner()" title="Minimize Notice" style="width:28px; height:28px;">
          ✕
        </button>
      </div>
    </div>

    <div class="iframe-stage">
      <iframe
        id="web-frame"
        sandbox="allow-scripts allow-same-origin allow-forms"
        allow="fullscreen; autoplay; clipboard-read; clipboard-write"
        referrerpolicy="no-referrer-when-downgrade"
        onload="onFrameLoad()"
      ></iframe>
    </div>
  </section>

  <!-- ==================== 3. FOCUS MODE ==================== -->
  <section id="view-focus" class="view">
    <header class="focus-header">
      <div class="focus-title-group">
        <span class="focus-badge">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
          </svg>
          Focus Mode
        </span>
        <span style="font-size:13px; color:var(--text-secondary);" class="hide-mobile">
          Distraction-free Study Notes &amp; Instant Wikipedia Summary
        </span>
      </div>

      <div style="display:flex; align-items:center; gap:8px;">
        <button id="btn-return-viewer" class="btn" onclick="returnToViewer()" style="display:none;">
          Return to Web Viewer
        </button>
        <button class="btn" onclick="showHome()">
          Home Dashboard
        </button>
        <button class="btn btn-accent" onclick="toggleFocusMode()">
          <span>Exit Focus</span>
          <span class="kbd-hint" style="background:rgba(15,23,42,0.45); color:#fff; border-color:rgba(255,255,255,0.2);">Esc</span>
        </button>
      </div>
    </header>

    <div class="focus-workspace">
      <!-- Left Panel: Client-Side Wikipedia Summary Reader -->
      <div class="focus-panel">
        <div class="panel-header">
          <h2>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>
            </svg>
            Wikipedia Quick Summary
          </h2>
          <button id="btn-insert-wiki" class="btn" onclick="insertSummaryToNotes()" style="padding: 4px 10px; font-size: 12px;" disabled>
            + Insert into Notes
          </button>
        </div>

        <form class="wiki-search-bar" onsubmit="handleWikiSearch(event)">
          <input
            id="wiki-query-input"
            type="text"
            placeholder="Search any concept (e.g., Photosynthesis, Pythagorean theorem)..."
            autocomplete="off"
          />
          <button type="submit" class="btn btn-accent">Lookup</button>
        </form>

        <div id="wiki-summary-output" class="wiki-content">
          <div class="wiki-article-title">Quick Reference Reader</div>
          <div class="wiki-article-desc">100% Client-Side Wikipedia Summary Fetcher</div>
          <p class="wiki-article-body">
            Type any academic topic above to fetch a clean, distraction-free encyclopedia summary without leaving Focus Mode. You can insert key takeaways directly into your study notes on the right.
          </p>
        </div>
      </div>

      <!-- Right Panel: Auto-Saved Study Notes -->
      <div class="focus-panel">
        <div class="panel-header">
          <h2>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#818cf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/>
            </svg>
            Study Notes
          </h2>
          <div style="display:flex; gap:6px;">
            <button class="btn" onclick="copyNotes()" style="padding: 4px 10px; font-size: 12px;">Copy</button>
            <button class="btn" onclick="downloadNotes()" style="padding: 4px 10px; font-size: 12px;">Download .md</button>
            <button class="btn" onclick="clearNotes()" style="padding: 4px 10px; font-size: 12px;">Clear</button>
          </div>
        </div>

        <textarea
          id="study-notes-area"
          class="notes-textarea"
          placeholder="Start typing your study notes, formulas, essay outlines, or key takeaways here... (Automatically saved in your browser)"
          oninput="handleNotesInput()"
        ></textarea>

        <div class="panel-footer">
          <span id="notes-save-status">Saved locally in browser</span>
          <span id="notes-stats">0 words · 0 chars</span>
        </div>
      </div>
    </div>
  </section>

  <script>
    // ==================== STATE ====================
    const STORAGE_KEY = "utopia_edu_study_notes_v1";
    const KNOWN_FRAME_BLOCKERS = [
      "khanacademy.org",
      "google.com",
      "youtube.com",
      "quizlet.com",
      "github.com",
      "coursera.org",
      "edx.org",
      "purdue.edu",
      "britannica.com",
      "loc.gov"
    ];

    let activeView = "home";
    let previousViewBeforeFocus = "home";
    let navHistory = [];
    let navIndex = -1;
    let currentWikiSummary = null;

    // ==================== DOM ELEMENTS ====================
    const viewHome = document.getElementById("view-home");
    const viewViewer = document.getElementById("view-viewer");
    const viewFocus = document.getElementById("view-focus");
    const webFrame = document.getElementById("web-frame");
    const viewerUrlInput = document.getElementById("viewer-url-input");
    const btnBack = document.getElementById("btn-back");
    const loadBar = document.getElementById("load-bar");
    const navNewTab = document.getElementById("nav-new-tab");
    const fallbackBanner = document.getElementById("fallback-banner");
    const fallbackMessage = document.getElementById("fallback-message");
    const fallbackNewTab = document.getElementById("fallback-new-tab");
    const fallbackDismiss = document.getElementById("fallback-dismiss");
    const btnReturnViewer = document.getElementById("btn-return-viewer");
    const notesArea = document.getElementById("study-notes-area");
    const notesStats = document.getElementById("notes-stats");
    const notesSaveStatus = document.getElementById("notes-save-status");

    // ==================== VIEW SWITCHING ====================
    function setActiveView(viewName) {
      activeView = viewName;
      viewHome.classList.toggle("active", viewName === "home");
      viewViewer.classList.toggle("active", viewName === "viewer");
      viewFocus.classList.toggle("active", viewName === "focus");

      if (viewName === "focus") {
        btnReturnViewer.style.display = navHistory.length > 0 ? "inline-flex" : "none";
        autoSyncWikiFromCurrentUrl();
        setTimeout(() => notesArea.focus(), 40);
      }
    }

    function showHome() {
      setActiveView("home");
    }

    function returnToViewer() {
      if (navHistory.length > 0) {
        setActiveView("viewer");
      } else {
        setActiveView("home");
      }
    }

    function toggleFocusMode() {
      if (activeView === "focus") {
        setActiveView(previousViewBeforeFocus || "home");
      } else {
        previousViewBeforeFocus = activeView;
        setActiveView("focus");
      }
    }

    // Escape key shortcut for Focus Mode
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        toggleFocusMode();
      }
    });

    // ==================== URL RESOLUTION & NAVIGATION ====================
    function resolveInputToUrl(raw) {
      const trimmed = (raw || "").trim();
      if (!trimmed) return "https://en.wikipedia.org/wiki/Main_Page";

      if (/^https?:\/\//i.test(trimmed)) {
        return trimmed;
      }

      // Looks like a domain name (contains dot and no spaces)
      if (!/\s/.test(trimmed) && /^[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+/.test(trimmed)) {
        return "https://" + trimmed;
      }

      // Treat search phrases as an embed-friendly Wikipedia search query
      return "https://en.wikipedia.org/w/index.php?search=" + encodeURIComponent(trimmed);
    }

    function isLikelyBlockedDomain(url) {
      try {
        const hostname = new URL(url).hostname.toLowerCase();
        return KNOWN_FRAME_BLOCKERS.some(
          (domain) => hostname === domain || hostname.endsWith("." + domain)
        );
      } catch {
        return false;
      }
    }

    function updateFallbackBanner(url) {
      fallbackNewTab.href = url;
      navNewTab.href = url;

      if (isLikelyBlockedDomain(url)) {
        fallbackBanner.classList.remove("compact");
        fallbackDismiss.style.display = "inline-flex";
        fallbackMessage.innerHTML =
          '<strong>Embedding Notice:</strong> This platform typically sets <strong>X-Frame-Options</strong> headers that block iframes. Click <strong>Open in New Tab ↗</strong> if the window below stays blank.';
      } else {
        fallbackBanner.classList.remove("compact");
        fallbackDismiss.style.display = "inline-flex";
        fallbackMessage.innerHTML =
          'Some websites restrict iframe embedding via <strong>X-Frame-Options</strong> headers. If the page below refuses to connect, open it directly in a new tab.';
      }
    }

    function collapseFallbackBanner() {
      fallbackBanner.classList.add("compact");
      fallbackDismiss.style.display = "none";
      fallbackMessage.innerHTML =
        "Viewing in sandboxed mode. Blocked by X-Frame-Options?";
    }

    function openResource(rawInput, pushHistory = true) {
      const targetUrl = resolveInputToUrl(rawInput);

      if (pushHistory) {
        if (navIndex < navHistory.length - 1) {
          navHistory = navHistory.slice(0, navIndex + 1);
        }
        if (navHistory[navIndex] !== targetUrl) {
          navHistory.push(targetUrl);
          navIndex = navHistory.length - 1;
        }
      }

      btnBack.disabled = navIndex <= 0;
      viewerUrlInput.value = targetUrl;
      updateFallbackBanner(targetUrl);

      setActiveView("viewer");
      startLoadingAnimation();
      webFrame.src = targetUrl;
    }

    function handleHomeSearch(event) {
      event.preventDefault();
      const input = document.getElementById("home-search-input");
      openResource(input.value, true);
    }

    function handleNavbarSubmit(event) {
      event.preventDefault();
      openResource(viewerUrlInput.value, true);
    }

    function goBack() {
      if (navIndex > 0) {
        navIndex -= 1;
        openResource(navHistory[navIndex], false);
      }
    }

    function reloadFrame() {
      if (navIndex >= 0 && navHistory[navIndex]) {
        startLoadingAnimation();
        webFrame.src = navHistory[navIndex];
      }
    }

    function startLoadingAnimation() {
      loadBar.classList.remove("done");
      loadBar.classList.add("loading");
    }

    function onFrameLoad() {
      loadBar.classList.remove("loading");
      loadBar.classList.add("done");
      setTimeout(() => loadBar.classList.remove("done"), 300);
    }

    function toggleFullscreen() {
      const elem = document.documentElement;
      if (!document.fullscreenElement) {
        if (elem.requestFullscreen) {
          elem.requestFullscreen().catch(() => {});
        }
      } else if (document.exitFullscreen) {
        document.exitFullscreen().catch(() => {});
      }
    }

    // ==================== FOCUS MODE: WIKIPEDIA SUMMARY ====================
    function autoSyncWikiFromCurrentUrl() {
      if (navIndex < 0) return;
      const currentUrl = navHistory[navIndex];
      try {
        const parsed = new URL(currentUrl);
        if (parsed.hostname.includes("wikipedia.org")) {
          if (parsed.pathname.startsWith("/wiki/")) {
            const rawTitle = decodeURIComponent(parsed.pathname.replace("/wiki/", "")).replace(/_/g, " ");
            if (rawTitle && !rawTitle.startsWith("Main Page") && !rawTitle.startsWith("Portal:")) {
              document.getElementById("wiki-query-input").value = rawTitle;
              fetchWikipediaSummary(rawTitle);
            }
          } else if (parsed.searchParams.get("search")) {
            const q = parsed.searchParams.get("search");
            document.getElementById("wiki-query-input").value = q;
            fetchWikipediaSummary(q);
          }
        }
      } catch {
        // Ignore invalid URLs
      }
    }

    function handleWikiSearch(event) {
      event.preventDefault();
      const query = document.getElementById("wiki-query-input").value.trim();
      if (query) {
        fetchWikipediaSummary(query);
      }
    }

    async function fetchWikipediaSummary(query) {
      const output = document.getElementById("wiki-summary-output");
      const insertBtn = document.getElementById("btn-insert-wiki");
      insertBtn.disabled = true;
      currentWikiSummary = null;

      output.innerHTML = `<p style="color:var(--text-secondary);">Searching Wikipedia for <strong>${escapeHtml(query)}</strong>...</p>`;

      try {
        // First resolve best matching title via CORS-enabled OpenSearch API
        const searchEndpoint =
          "https://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=json&origin=*&search=" +
          encodeURIComponent(query);
        const searchRes = await fetch(searchEndpoint);
        const searchData = await searchRes.json();
        const matchedTitle = (searchData && searchData[1] && searchData[1][0]) ? searchData[1][0] : query;

        // Fetch clean REST API summary
        const summaryEndpoint =
          "https://en.wikipedia.org/api/rest_v1/page/summary/" + encodeURIComponent(matchedTitle);
        const res = await fetch(summaryEndpoint);
        if (!res.ok) throw new Error("Article not found");
        const data = await res.json();

        currentWikiSummary = {
          title: data.title || matchedTitle,
          description: data.description || "Wikipedia Encyclopedia Summary",
          extract: data.extract || "No summary text available for this entry.",
          url: (data.content_urls && data.content_urls.desktop && data.content_urls.desktop.page) ||
               "https://en.wikipedia.org/wiki/" + encodeURIComponent(matchedTitle)
        };

        output.innerHTML = `
          <div class="wiki-article-title">${escapeHtml(currentWikiSummary.title)}</div>
          <div class="wiki-article-desc">${escapeHtml(currentWikiSummary.description)}</div>
          <p class="wiki-article-body">${escapeHtml(currentWikiSummary.extract)}</p>
          <button class="btn" onclick="openResource('${currentWikiSummary.url.replace(/'/g, "\\'")}')">
            Open Full Article in Viewer
          </button>
        `;
        insertBtn.disabled = false;
      } catch {
        output.innerHTML = `
          <div class="wiki-article-title">No Exact Match Found</div>
          <p class="wiki-article-body">
            Could not retrieve an instant summary for "<strong>${escapeHtml(query)}</strong>". Try a broader keyword or open a full Wikipedia search in the viewer.
          </p>
        `;
      }
    }

    function insertSummaryToNotes() {
      if (!currentWikiSummary) return;
      const snippet = `\n\n### ${currentWikiSummary.title}\n${currentWikiSummary.extract}\n(Source: ${currentWikiSummary.url})\n`;
      notesArea.value = (notesArea.value.trimEnd() + snippet).trimStart();
      handleNotesInput();
      notesArea.scrollTop = notesArea.scrollHeight;
    }

    function escapeHtml(str) {
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
    }

    // ==================== FOCUS MODE: STUDY NOTES ====================
    function loadSavedNotes() {
      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved !== null) {
          notesArea.value = saved;
        }
      } catch {
        // Ignore storage restrictions
      }
      updateNotesStats();
    }

    function handleNotesInput() {
      try {
        localStorage.setItem(STORAGE_KEY, notesArea.value);
        notesSaveStatus.textContent = "Saved locally · " + new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      } catch {
        notesSaveStatus.textContent = "Session memory only";
      }
      updateNotesStats();
    }

    function updateNotesStats() {
      const text = notesArea.value;
      const words = text.trim() ? text.trim().split(/\s+/).length : 0;
      notesStats.textContent = `${words} words · ${text.length} chars`;
    }

    function copyNotes() {
      if (!notesArea.value) return;
      navigator.clipboard?.writeText(notesArea.value);
      notesSaveStatus.textContent = "Copied to clipboard!";
    }

    function downloadNotes() {
      const blob = new Blob([notesArea.value || "# Study Notes\n"], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "utopia-study-notes.md";
      a.click();
      URL.revokeObjectURL(url);
    }

    function clearNotes() {
      if (!notesArea.value) return;
      notesArea.value = "";
      handleNotesInput();
    }

    // Initialize saved notes on startup
    loadSavedNotes();
  </script>
</body>
</html>
"""

components.html(HTML_APP, height=950, scrolling=False)
