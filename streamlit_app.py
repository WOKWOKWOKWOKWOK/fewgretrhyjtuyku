import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Utopia Education",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
            display: none !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100vw !important;
        }
        iframe {
            display: block;
            border: none;
            width: 100vw;
            height: 100vh;
        }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            background-color: #0f172a;
        }
    </style>
    """,
    unsafe_allow_html=True
)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Utopia Education</title>
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
    body, html { width: 100vw; height: 100vh; overflow: hidden; background: #0f172a; color: #f8fafc; display: flex; flex-direction: column; }
    #toolbar { height: 48px; background: #1e293b; border-bottom: 1px solid #334155; display: flex; align-items: center; padding: 0 12px; gap: 8px; z-index: 100; transition: margin-top 0.2s ease; }
    #toolbar.hidden { margin-top: -48px; }
    .btn { background: #334155; color: #f8fafc; border: 1px solid #475569; border-radius: 6px; padding: 6px 12px; font-size: 13px; font-weight: 500; cursor: pointer; white-space: nowrap; }
    .btn:hover { background: #475569; }
    .btn-primary { background: #4f46e5; border-color: #6366f1; }
    .btn-primary:hover { background: #4338ca; }
    .btn-shield-on { background: #065f46; border-color: #10b981; color: #d1fae5; }
    .btn-panic { background: #991b1b; border-color: #ef4444; color: #fee2e2; }
    #url-form { flex: 1; display: flex; gap: 6px; }
    #url-input { flex: 1; background: #0f172a; border: 1px solid #475569; border-radius: 6px; padding: 6px 12px; color: #f8fafc; font-size: 13px; outline: none; }
    #url-input:focus { border-color: #6366f1; }
    #show-toolbar-btn { position: fixed; top: 8px; right: 12px; background: rgba(30, 41, 59, 0.9); color: #cbd5e1; border: 1px solid #475569; border-radius: 20px; padding: 4px 12px; font-size: 12px; cursor: pointer; z-index: 90; display: none; }
    #viewport-container { flex: 1; position: relative; width: 100%; height: 100%; background: #0f172a; }
    #web-frame { width: 100%; height: 100%; border: none; background: #ffffff; }
    #fallback-bar { background: #1e1b4b; border-bottom: 1px solid #4338ca; padding: 6px 16px; font-size: 12px; color: #c7d2fe; display: flex; justify-content: space-between; align-items: center; }
    #decoy-screen { display: none; position: fixed; inset: 0; background: #ffffff; color: #202122; z-index: 9999; overflow-y: auto; padding: 32px 10%; font-family: Georgia, serif; line-height: 1.6; }
    #decoy-screen h1 { font-size: 28px; border-bottom: 1px solid #a2a9b1; padding-bottom: 6px; margin-bottom: 16px; font-weight: normal; }
    #decoy-screen p { font-family: sans-serif; font-size: 15px; margin-bottom: 14px; }
    .decoy-header { display: flex; justify-content: space-between; align-items: center; font-family: sans-serif; font-size: 12px; color: #54595d; margin-bottom: 20px; border-bottom: 1px solid #eaecf0; padding-bottom: 8px; }
</style>
</head>
<body>
    <div id="toolbar">
        <button class="btn btn-primary" onclick="loadUrl('https://utopiaweb.org')">Utopia Home</button>
        <button class="btn" onclick="reloadFrame()">↻</button>
        <form id="url-form" onsubmit="handleUrlSubmit(event)">
            <input type="text" id="url-input" value="https://utopiaweb.org" placeholder="Enter URL or mirror link..." />
            <button type="submit" class="btn">Go</button>
        </form>
        <button id="shield-btn" class="btn btn-shield-on" onclick="togglePopupShield()">🛡 Popups: Blocked</button>
        <button class="btn" onclick="openBlankTab()">↗ Blank Tab</button>
        <button class="btn" onclick="toggleFullscreen()">⛶</button>
        <button class="btn" onclick="toggleToolbar()">▲</button>
        <button class="btn btn-panic" onclick="toggleDecoy()">Hide (Esc)</button>
    </div>

    <div id="fallback-bar">
        <span>Tip: If a website refuses to connect inside the frame, click <strong>↗ Blank Tab</strong> to launch it directly.</span>
        <span style="cursor:pointer;" onclick="this.parentElement.style.display='none'">✕</span>
    </div>

    <button id="show-toolbar-btn" onclick="toggleToolbar()">▼ Show Bar</button>

    <div id="viewport-container">
        <iframe id="web-frame" src="https://utopiaweb.org" sandbox="allow-scripts allow-same-origin allow-forms allow-pointer-lock" allow="fullscreen; autoplay; clipboard-read; clipboard-write; gamepad"></iframe>
    </div>

    <div id="decoy-screen">
        <div class="decoy-header">
            <span><strong>WIKIPEDIA</strong> — The Free Encyclopedia</span>
            <button onclick="toggleDecoy()" style="padding:4px 10px; cursor:pointer;">Return to Portal (Esc)</button>
        </div>
        <h1>George Washington</h1>
        <p><strong>George Washington</strong> (February 22, 1732 – December 14, 1799) was an American Founding Father, military officer, and politician who served as the first president of the United States from 1789 to 1797. Appointed by the Second Continental Congress as commander of the Continental Army in June 1775, Washington led Patriot forces to victory in the American Revolutionary War.</p>
        <p>As the first president of the United States, Washington implemented a strong, well-financed national government while remaining neutral in a fierce rivalry that emerged between cabinet members Thomas Jefferson and Alexander Hamilton. He set enduring precedents for the office of president, including republicanism, a peaceful transfer of power, and the two-term tradition.</p>
    </div>
<script>
    const frame = document.getElementById('web-frame');
    const urlInput = document.getElementById('url-input');
    const toolbar = document.getElementById('toolbar');
    const showToolbarBtn = document.getElementById('show-toolbar-btn');
    const shieldBtn = document.getElementById('shield-btn');
    const decoyScreen = document.getElementById('decoy-screen');
    let blockPopups = true;
    let isDecoyActive = false;

    function formatUrl(input) {
        let trimmed = input.trim();
        if (!trimmed) return 'https://utopiaweb.org';
        if (!trimmed.startsWith('http://') && !trimmed.startsWith('https://')) {
            return (trimmed.includes('.') && !trimmed.includes(' ')) ? 'https://' + trimmed : 'https://duckduckgo.com' + encodeURIComponent(trimmed);
        }
        return trimmed;
    }

    function loadUrl(rawUrl) {
        const finalUrl = formatUrl(rawUrl);
        urlInput.value = finalUrl;
        frame.src = finalUrl;
        frame.focus();
    }

    function handleUrlSubmit(e) { e.preventDefault(); loadUrl(urlInput.value); }

    function reloadFrame() {
        const current = urlInput.value;
        frame.src = 'about:blank';
        setTimeout(() => { frame.src = formatUrl(current); frame.focus(); }, 50);
    }

    function togglePopupShield() {
        blockPopups = !blockPopups;
        if (blockPopups) {
            frame.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms allow-pointer-lock');
            shieldBtn.textContent = '🛡 Popups: Blocked';
            shieldBtn.className = 'btn btn-shield-on';
        } else {
            frame.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms allow-pointer-lock allow-popups allow-popups-to-escape-sandbox');
            shieldBtn.textContent = '⚠ Popups: Allowed';
            shieldBtn.className = 'btn';
        }
        reloadFrame();
    }

    function openBlankTab() {
        const targetUrl = formatUrl(urlInput.value);
        const win = window.open('about:blank', '_blank');
        if (win) {
            win.document.title = "Google Classroom";
            const iframe = win.document.createElement('iframe');
            iframe.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;border:none;';
            iframe.src = targetUrl;
            win.document.body.style.margin = '0';
            win.document.body.appendChild(iframe);
        } else {
            alert("Pop-up blocked! Allow pop-ups for this app to use Blank Tab mode.");
        }
    }

    function toggleToolbar() {
        toolbar.classList.toggle('hidden');
        showToolbarBtn.style.display = toolbar.classList.contains('hidden') ? 'block' : 'none';
    }

    function toggleFullscreen() {
        if (!document.fullscreenElement) { document.documentElement.requestFullscreen().catch(() => {}); }
        else { document.exitFullscreen().catch(() => {}); }
    }

    function toggleDecoy() {
        isDecoyActive = !isDecoyActive;
        decoyScreen.style.display = isDecoyActive ? 'block' : 'none';
        const newTitle = isDecoyActive ? "George Washington - Wikipedia" : "Utopia Education";
        try { window.parent.document.title = newTitle; } catch(e) {}
        document.title = newTitle;
        if (!isDecoyActive) frame.focus();
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' || e.key === '~' || e.key === '`') toggleDecoy();
    });
</script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
