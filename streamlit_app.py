import html
import re
import urllib.parse
from typing import Dict, List, Tuple

import requests
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup, Tag

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION (Must be the first Streamlit command)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Utopia Education",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# 2. CONSTANTS, AD-BLOCKER RULES & PORTAL CONTENT
# -----------------------------------------------------------------------------
AD_DOMAINS = (
    "doubleclick.net",
    "googlesyndication.com",
    "google-analytics.com",
    "googletagmanager.com",
    "googletagservices.com",
    "adservice.google.com",
    "pagead2.googlesyndication.com",
    "adnxs.com",
    "taboola.com",
    "outbrain.com",
    "criteo.com",
    "criteo.net",
    "amazon-adsystem.com",
    "popads.net",
    "popcash.net",
    "propellerads.com",
    "adsterra.com",
    "mgid.com",
    "revcontent.com",
    "pubmatic.com",
    "rubiconproject.com",
    "openx.net",
    "casalemedia.com",
    "moatads.com",
    "scorecardresearch.com",
    "quantserve.com",
    "hotjar.com",
    "connect.facebook.net",
    "ads-twitter.com",
    "bat.bing.com",
    "zedo.com",
    "adroll.com",
    "bidswitch.net",
    "sharethrough.com",
    "triplelift.com",
    "mediavine.com",
    "adthrive.com",
    "ezoic.net",
    "smartadserver.com",
    "advertising.com",
    "yieldmo.com",
    "indexexchange.com",
    "33across.com",
    "sovrn.com",
)

AD_TOKEN_PATTERN = re.compile(
    r"(^|[-_])(ad|ads|advert|advertisement|adsbygoogle|google_ads|div-gpt-ad|"
    r"sponsor|sponsored|taboola|outbrain|banner-ad|ad-banner|ad-slot|ad-unit|"
    r"ad-container|ad-wrapper|popup-ad|popunder|interstitial-ad)($|[-_])",
    re.IGNORECASE,
)

AD_SCRIPT_SIGNATURES = (
    "adsbygoogle",
    "googletag.cmd",
    "googletag.display",
    "fbq(",
    "gtag('config'",
    'gtag("config"',
    "_taboola",
    "outbrain",
    "popads",
    "criteo",
    "amazon-adsystem",
    "prebid",
    "pbjs.",
)

COSMETIC_FILTER_CSS = """
<style id="utopia-adblock-cosmetic">
  ins.adsbygoogle,
  [id*="google_ads"],
  [id*="div-gpt-ad"],
  [id*="taboola"],
  [id*="outbrain"],
  [class*="banner-ad"],
  [class*="ad-banner"],
  [class*="ad-slot"],
  [class*="ad-container"],
  [class*="ad-wrapper"],
  [class*="sponsored-content"],
  [data-ad],
  [data-ad-slot],
  [data-google-query-id],
  iframe[src*="doubleclick"],
  iframe[src*="googlesyndication"],
  iframe[src*="taboola"],
  iframe[src*="outbrain"],
  .adsbygoogle,
  .ad-overlay,
  .popup-overlay {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
  }
</style>
"""

SUBJECT_CARDS = [
    {
        "icon": "📐",
        "title": "Math & Algebra",
        "desc": "Interactive equations, algebra step-by-step guides, geometry, and calculus references.",
        "tag": "mathsisfun.com",
        "url": "https://www.mathsisfun.com/algebra/index.html",
    },
    {
        "icon": "🏛️",
        "title": "Historical Research",
        "desc": "World civilizations, primary historical archives, timelines, and documented eras.",
        "tag": "wikipedia.org",
        "url": "https://en.wikipedia.org/wiki/Portal:History",
    },
    {
        "icon": "🔬",
        "title": "Science Lab",
        "desc": "Open-access textbooks and modules for Biology, Chemistry, Physics, and Astronomy.",
        "tag": "openstax.org",
        "url": "https://openstax.org/subjects/science",
    },
    {
        "icon": "📖",
        "title": "Literature Themes",
        "desc": "Classic novels, poetry collections, dramatic works, and literary analysis resources.",
        "tag": "gutenberg.org",
        "url": "https://www.gutenberg.org/",
    },
    {
        "icon": "🌍",
        "title": "Social Studies",
        "desc": "Civics, government systems, economics, human geography, and cultural studies.",
        "tag": "wikipedia.org",
        "url": "https://en.wikipedia.org/wiki/Portal:Social_sciences",
    },
    {
        "icon": "✍️",
        "title": "Essay Writing",
        "desc": "Thesis development, academic rhetoric, grammar mechanics, and MLA/APA citations.",
        "tag": "owl.purdue.edu",
        "url": "https://owl.purdue.edu/owl/general_writing/index.html",
    },
]

DECOY_WIKIPEDIA_HTML = """
<div id="utopia-decoy-page" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Lato, Helvetica, Arial, sans-serif; background: #ffffff; color: #202122; margin: 0; padding: 0; line-height: 1.6; min-height: 100vh;">
  <div style="background: #f8f9fa; border-bottom: 1px solid #a2a9b1; padding: 10px 24px; display: flex; align-items: center; justify-content: space-between;">
    <div style="display: flex; align-items: center; gap: 14px;">
      <span style="font-size: 20px; font-weight: 700; font-family: Georgia, serif; letter-spacing: 0.5px;">WIKIPEDIA</span>
      <span style="font-size: 12px; color: #54595d;">The Free Encyclopedia</span>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
      <input type="text" value="George Washington" readonly style="border: 1px solid #a2a9b1; border-radius: 2px; padding: 5px 10px; font-size: 13px; width: 240px; background: #fff; color: #202122;" />
      <span style="font-size: 12px; color: #3366cc; cursor: pointer;" onclick="window.utopiaRestore && window.utopiaRestore()">Log in</span>
    </div>
  </div>
  <div style="max-width: 1180px; margin: 0 auto; padding: 20px 28px; display: grid; grid-template-columns: 190px 1fr; gap: 28px;">
    <aside style="font-size: 13px; color: #202122; border-right: 1px solid #eaecf0; padding-right: 14px;">
      <div style="font-weight: 700; border-bottom: 1px solid #eaecf0; padding-bottom: 6px; margin-bottom: 10px;">Contents</div>
      <ul style="list-style: none; padding: 0; margin: 0; line-height: 1.9; color: #3366cc;">
        <li>(Top)</li>
        <li>1 Early life (1732–1752)</li>
        <li>2 Colonial military career</li>
        <li>3 American Revolution</li>
        <li>4 Presidency (1789–1797)</li>
        <li>5 Retirement and death</li>
        <li>6 Legacy and memorials</li>
        <li>7 References</li>
      </ul>
    </aside>
    <main>
      <h1 style="font-family: Georgia, 'Times New Roman', serif; font-size: 29px; font-weight: 400; border-bottom: 1px solid #a2a9b1; margin: 0 0 8px 0; padding-bottom: 4px;">George Washington</h1>
      <div style="font-size: 12.5px; color: #54595d; margin-bottom: 16px;">From Wikipedia, the free encyclopedia</div>
      <div style="float: right; width: 260px; background: #f8f9fa; border: 1px solid #a2a9b1; padding: 10px; margin: 0 0 16px 20px; font-size: 12.5px;">
        <div style="text-align: center; font-weight: 700; font-size: 14px; background: #eaecf0; padding: 5px; margin-bottom: 8px;">George Washington</div>
        <div style="background: #e2e8f0; height: 150px; display: flex; align-items: center; justify-content: center; color: #475569; font-family: Georgia, serif; font-style: italic; margin-bottom: 8px; border: 1px solid #cbd5e1;">
          Portrait by Gilbert Stuart (1796)
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
          <tr><td colspan="2" style="background: #eaecf0; text-align: center; font-weight: 700; padding: 4px;">1st President of the United States</td></tr>
          <tr><td style="padding: 4px 0; font-weight: 600;">In office</td><td style="padding: 4px 0;">April 30, 1789 – March 4, 1797</td></tr>
          <tr><td style="padding: 4px 0; font-weight: 600;">Vice President</td><td style="padding: 4px 0;">John Adams</td></tr>
          <tr><td style="padding: 4px 0; font-weight: 600;">Preceded by</td><td style="padding: 4px 0;"><i>Office established</i></td></tr>
          <tr><td style="padding: 4px 0; font-weight: 600;">Succeeded by</td><td style="padding: 4px 0;">John Adams</td></tr>
          <tr><td style="padding: 4px 0; font-weight: 600;">Born</td><td style="padding: 4px 0;">February 22, 1732<br/>Popes Creek, Virginia</td></tr>
          <tr><td style="padding: 4px 0; font-weight: 600;">Died</td><td style="padding: 4px 0;">December 14, 1799 (aged 67)<br/>Mount Vernon, Virginia</td></tr>
        </table>
      </div>
      <p style="margin-top: 0;">
        <b>George Washington</b> (February 22, 1732 – December 14, 1799) was an American Founding Father, military officer, and statesman who served as the first president of the United States from 1789 to 1797. Appointed by the Second Continental Congress as commander of the Continental Army in 1775, Washington led Patriot forces to victory in the American Revolutionary War and then served as president of the Constitutional Convention in 1787, which drafted the current Constitution of the United States.
      </p>
      <p>
        Washington's first public office, from 1749 to 1750, was as surveyor of Culpeper County in the Colony of Virginia. In 1752, he received military training and was granted the rank of major in the Virginia Regiment. During the French and Indian War, Washington was promoted to colonel in 1758 and commanded the Virginia Regiment, gaining invaluable command experience across the frontier.
      </p>
      <h2 style="font-family: Georgia, serif; font-size: 21px; font-weight: 400; border-bottom: 1px solid #a2a9b1; padding-bottom: 3px; margin-top: 22px;">Presidency (1789–1797)</h2>
      <p>
        Washington was unanimously elected president by the Electoral College in both the 1788–1789 and 1792 elections. As the first U.S. president, Washington implemented a strong, well-financed national government while remaining impartial in a fierce rivalry that emerged between cabinet members Thomas Jefferson and Alexander Hamilton. During the French Revolution, he proclaimed a policy of neutrality while also sanctioning the Jay Treaty.
      </p>
      <p>
        He set enduring precedents for the office of the president, including republicanism, a peaceful transfer of power, the use of the title "Mr. President", and the two-term tradition. His 1796 Farewell Address became a preeminent statement on republicanism, warning against partisanship, sectionalism, and entanglement in foreign wars.
      </p>
      <div style="margin-top: 32px; padding-top: 12px; border-top: 1px solid #eaecf0; font-size: 11.5px; color: #54595d; display: flex; justify-content: space-between;">
        <span>This page was last edited on November 10, 2026, at 14:22 (UTC).</span>
        <span style="color: #3366cc; cursor: pointer;" onclick="window.utopiaRestore && window.utopiaRestore()">[Press Esc or ~ to resume session]</span>
      </div>
    </main>
  </div>
</div>
"""


# -----------------------------------------------------------------------------
# 3. SESSION STATE & QUERY PARAM NAVIGATION
# -----------------------------------------------------------------------------
def init_session_state() -> None:
    defaults = {
        "view_mode": "home",  # "home" or "browser"
        "current_url": "",
        "history": [],
        "history_index": -1,
        "adblock_enabled": True,
        "render_mode": "proxy",  # "proxy" or "iframe"
        "panic_active": False,
        "reload_nonce": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def normalize_input(raw_query: str) -> str:
    """Convert raw user input into a valid URL or a frame-friendly search URL."""
    query = (raw_query or "").strip()
    if not query:
        return ""

    if query.startswith(("http://", "https://")):
        return query

    # Check if input looks like a domain/URL (e.g., wikipedia.org, khanacademy.org/math)
    domain_pattern = re.compile(
        r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s]*)?$"
    )
    if " " not in query and domain_pattern.match(query):
        return f"https://{query}"

    # Route search queries to DuckDuckGo HTML (fast, clean, no JS/X-Frame-Options lockouts)
    encoded = urllib.parse.quote_plus(query)
    return f"https://html.duckduckgo.com/html/?q={encoded}"


def navigate_to(raw_input: str, push_history: bool = True) -> None:
    """Navigate the browser viewer to a URL or search query."""
    target_url = normalize_input(raw_input)
    if not target_url:
        return

    st.session_state.view_mode = "browser"
    st.session_state.current_url = target_url
    st.session_state.render_mode = "proxy"

    if push_history:
        history: List[str] = st.session_state.history
        idx: int = st.session_state.history_index
        # Truncate forward history if branching
        if idx < len(history) - 1:
            history = history[: idx + 1]
        if not history or history[-1] != target_url:
            history.append(target_url)
        st.session_state.history = history
        st.session_state.history_index = len(history) - 1


def go_back() -> None:
    if st.session_state.history_index > 0:
        st.session_state.history_index -= 1
        st.session_state.current_url = st.session_state.history[
            st.session_state.history_index
        ]
        st.session_state.view_mode = "browser"


def go_forward() -> None:
    if st.session_state.history_index < len(st.session_state.history) - 1:
        st.session_state.history_index += 1
        st.session_state.current_url = st.session_state.history[
            st.session_state.history_index
        ]
        st.session_state.view_mode = "browser"


def go_home() -> None:
    st.session_state.view_mode = "home"


def handle_query_param_navigation() -> None:
    """Handle link clicks dispatched from inside the proxied web frame."""
    nav_target = st.query_params.get("nav")
    if nav_target:
        st.query_params.clear()
        navigate_to(nav_target, push_history=True)


# -----------------------------------------------------------------------------
# 4. BUILT-IN AD & TRACKER BLOCKER + ASSET REWRITER
# -----------------------------------------------------------------------------
def is_ad_url(url: str) -> bool:
    if not url:
        return False
    lower = url.lower()
    if any(domain in lower for domain in AD_DOMAINS):
        return True
    if any(
        token in lower
        for token in (
            "/pagead/",
            "/ads/",
            "/adserver",
            "/adservice",
            "doubleclick",
            "googlesyndication",
            "analytics.js",
            "gtm.js",
            "fbevents.js",
        )
    ):
        return True
    return False


def has_ad_attributes(tag: Tag) -> bool:
    if not isinstance(tag, Tag) or tag.name in ("html", "body", "head"):
        return False

    if tag.name == "ins" and "adsbygoogle" in (tag.get("class") or []):
        return True

    if tag.has_attr("data-ad") or tag.has_attr("data-ad-slot") or tag.has_attr("data-google-query-id"):
        return True

    aria_label = tag.get("aria-label", "")
    if isinstance(aria_label, str) and "advertisement" in aria_label.lower():
        return True

    tag_id = tag.get("id", "")
    if isinstance(tag_id, str) and tag_id and AD_TOKEN_PATTERN.search(tag_id):
        return True

    classes = tag.get("class") or []
    if isinstance(classes, str):
        classes = classes.split()
    for cls in classes:
        if AD_TOKEN_PATTERN.search(cls):
            return True

    return False


def resolve_url(raw_url: str, base_url: str) -> str:
    """Resolve relative URLs and unwrap DuckDuckGo redirect links."""
    if not raw_url:
        return raw_url
    cleaned = raw_url.strip()
    if cleaned.startswith(("data:", "javascript:", "mailto:", "tel:", "#")):
        return cleaned

    absolute = urllib.parse.urljoin(base_url, cleaned)

    # Unwrap DuckDuckGo HTML redirect URLs so search results load directly in-proxy
    parsed = urllib.parse.urlparse(absolute)
    if "duckduckgo.com" in parsed.netloc and parsed.path.startswith("/l/"):
        qs = urllib.parse.parse_qs(parsed.query)
        if "uddg" in qs and qs["uddg"]:
            return qs["uddg"][0]

    return absolute


def rewrite_srcset(srcset_val: str, base_url: str) -> str:
    parts = []
    for candidate in srcset_val.split(","):
        tokens = candidate.strip().split()
        if not tokens:
            continue
        tokens[0] = resolve_url(tokens[0], base_url)
        parts.append(" ".join(tokens))
    return ", ".join(parts)


def rewrite_css_urls(css_text: str, base_url: str) -> str:
    def _repl(match: re.Match) -> str:
        quote = match.group(1) or ""
        raw = match.group(2).strip()
        if raw.startswith(("data:", "#")):
            return match.group(0)
        resolved = resolve_url(raw, base_url)
        return f"url({quote}{resolved}{quote})"

    return re.sub(r"""url\(\s*(['"]?)(.*?)\1\s*\)""", _repl, css_text, flags=re.IGNORECASE)


def build_frame_bridge_script(base_url: str, adblock_enabled: bool) -> str:
    """Inject lightweight JS inside the rendered page for seamless navigation & panic hotkey."""
    safe_base = html.escape(base_url, quote=True)
    anti_popup = "window.open = function() { return null; };" if adblock_enabled else ""
    return f"""
<script id="utopia-frame-bridge">
(function() {{
  {anti_popup}
  const BASE_URL = "{safe_base}";

  function triggerParentPanic() {{
    try {{
      if (window.parent && typeof window.parent.__utopiaTogglePanic === "function") {{
        window.parent.__utopiaTogglePanic(true);
      }}
    }} catch (err) {{}}
  }}

  // Instant Escape or ~ panic hotkey inside web viewer
  window.addEventListener("keydown", function(e) {{
    if (e.key === "Escape" || e.key === "~" || e.key === "`") {{
      e.preventDefault();
      e.stopPropagation();
      triggerParentPanic();
    }}
  }}, true);

  function navigateParent(targetUrl) {{
    if (!targetUrl || targetUrl.startsWith("javascript:") || targetUrl.startsWith("mailto:") || targetUrl.startsWith("tel:")) {{
      return false;
    }}
    if (targetUrl.startsWith("#")) {{
      const el = document.querySelector(targetUrl);
      if (el) el.scrollIntoView({{ behavior: "smooth" }});
      return true;
    }}
    try {{
      const resolved = new URL(targetUrl, BASE_URL).href;
      const topUrl = new URL(window.top.location.href);
      topUrl.searchParams.set("nav", resolved);
      window.top.location.href = topUrl.toString();
      return true;
    }} catch (err) {{
      return false;
    }}
  }}

  // Intercept link clicks for ultra-smooth ad-blocked navigation
  document.addEventListener("click", function(e) {{
    const anchor = e.target.closest("a[href]");
    if (!anchor) return;
    const href = anchor.getAttribute("href");
    if (!href || href.startsWith("#")) return;
    if (navigateParent(href)) {{
      e.preventDefault();
      e.stopPropagation();
    }}
  }}, true);

  // Intercept GET forms (e.g., on-page search bars)
  document.addEventListener("submit", function(e) {{
    const form = e.target;
    if (!form || (form.method && form.method.toLowerCase() !== "get")) return;
    const action = form.getAttribute("action") || BASE_URL;
    try {{
      const actionUrl = new URL(action, BASE_URL);
      const formData = new FormData(form);
      for (const [k, v] of formData.entries()) {{
        actionUrl.searchParams.set(k, v.toString());
      }}
      if (navigateParent(actionUrl.href)) {{
        e.preventDefault();
        e.stopPropagation();
      }}
    }} catch (err) {{}}
  }}, true);
}})();
</script>
"""


@st.cache_data(ttl=180, show_spinner=False)
def fetch_and_clean_page(
    url: str, adblock_enabled: bool, reload_nonce: int = 0
) -> Dict[str, object]:
    """
    Fetch target webpage, strip ads/trackers, rewrite relative assets to absolute URLs,
    or gracefully fall back to direct sandboxed iframe mode when required.
    """
    _ = reload_nonce  # Used solely to bust Streamlit cache on manual reload

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/128.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "DNT": "1",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=(6, 12), allow_redirects=True)
    except requests.RequestException as exc:
        return {
            "mode": "iframe",
            "url": url,
            "blocked_count": 0,
            "title": url,
            "notice": f"Switched to Direct Frame mode ({exc.__class__.__name__}).",
        }

    # If site blocks automated requests (401/403/429/503) or returns non-HTML, use Direct Frame
    content_type = resp.headers.get("Content-Type", "").lower()
    if resp.status_code in (401, 403, 429, 503) or (
        "text/html" not in content_type and "application/xhtml" not in content_type
    ):
        return {
            "mode": "iframe",
            "url": resp.url or url,
            "blocked_count": 0,
            "title": resp.url or url,
            "notice": f"Switched to Direct Frame mode (HTTP {resp.status_code}).",
        }

    resp.encoding = resp.apparent_encoding or resp.encoding or "utf-8"
    final_url = resp.url or url
    soup = BeautifulSoup(resp.text, "html.parser")
    blocked_count = 0

    # 1. Strip restrictive frame/CSP meta tags
    for meta in soup.find_all("meta"):
        http_equiv = (meta.get("http-equiv") or "").lower()
        if http_equiv in ("content-security-policy", "x-frame-options"):
            meta.decompose()

    # 2. Built-in Ad & Tracker Blocker
    if adblock_enabled:
        # Remove ad/tracker network scripts, iframes, beacons, and stylesheets
        for tag in list(
            soup.find_all(["script", "iframe", "img", "link", "object", "embed", "source"])
        ):
            if not isinstance(tag, Tag) or tag.attrs is None:
                continue
            src_val = (
                tag.get("src")
                or tag.get("href")
                or tag.get("data")
                or tag.get("data-src")
                or ""
            )
            if isinstance(src_val, str) and is_ad_url(src_val):
                tag.decompose()
                blocked_count += 1
                continue

            if tag.name == "script" and tag.string:
                script_body = tag.string.lower()
                if any(sig in script_body for sig in AD_SCRIPT_SIGNATURES):
                    tag.decompose()
                    blocked_count += 1
                    continue

        # Remove HTML elements matching ad/sponsor/popup class or ID tokens
        for tag in list(soup.find_all(True)):
            if not isinstance(tag, Tag) or tag.attrs is None:
                continue
            if has_ad_attributes(tag):
                tag.decompose()
                blocked_count += 1

    # 3. Rewrite relative URLs across HTML attributes & inline styles
    url_attrs = ("href", "src", "action", "data-src", "poster")
    for tag in soup.find_all(True):
        if not isinstance(tag, Tag) or tag.attrs is None:
            continue

        for attr in url_attrs:
            val = tag.get(attr)
            if isinstance(val, str) and val.strip():
                tag[attr] = resolve_url(val, final_url)

        if tag.has_attr("srcset") and isinstance(tag["srcset"], str):
            tag["srcset"] = rewrite_srcset(tag["srcset"], final_url)

        if tag.has_attr("style") and isinstance(tag["style"], str):
            tag["style"] = rewrite_css_urls(tag["style"], final_url)

    for style_tag in soup.find_all("style"):
        if style_tag.string:
            style_tag.string = rewrite_css_urls(style_tag.string, final_url)

    # 4. Inject Cosmetic Ad-Block CSS & Seamless Navigation/Panic Bridge into <head>
    head = soup.head
    if head is None:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)

    if adblock_enabled:
        head.append(BeautifulSoup(COSMETIC_FILTER_CSS, "html.parser"))

    head.append(
        BeautifulSoup(
            build_frame_bridge_script(final_url, adblock_enabled), "html.parser"
        )
    )

    page_title = (
        soup.title.string.strip()
        if soup.title and soup.title.string
        else final_url
    )

    return {
        "mode": "proxy",
        "html": str(soup),
        "blocked_count": blocked_count,
        "title": page_title,
        "url": final_url,
    }


# -----------------------------------------------------------------------------
# 5. CUSTOM DARK-MODE CSS & INSTANT PANIC ENGINE
# -----------------------------------------------------------------------------
def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        /* Hide all default Streamlit chrome */
        header[data-testid="stHeader"],
        #MainMenu,
        footer,
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton {
            display: none !important;
            visibility: hidden !important;
        }

        /* Deep Navy / Slate Base Theme */
        html, body, .stApp {
            background-color: #0f172a !important;
            color: #f8fafc !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .block-container {
            padding-top: 0.45rem !important;
            padding-bottom: 0.25rem !important;
            padding-left: 0.9rem !important;
            padding-right: 0.9rem !important;
            max-width: 100% !important;
        }

        /* Sleek Inputs & Buttons */
        div[data-testid="stTextInput"] input {
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: 1px solid rgba(99, 102, 241, 0.45) !important;
            border-radius: 10px !important;
            padding: 0.52rem 0.9rem !important;
            font-size: 0.94rem !important;
            box-shadow: 0 0 18px rgba(99, 102, 241, 0.16) !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 24px rgba(99, 102, 241, 0.45) !important;
            outline: none !important;
        }

        div[data-testid="stTextInput"] label {
            display: none !important;
        }

        /* Primary & Secondary Streamlit Buttons */
        .stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(99, 102, 241, 0.35) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
            padding: 0.42rem 0.75rem !important;
            transition: all 0.18s ease !important;
            white-space: nowrap !important;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            border-color: #6366f1 !important;
            background: rgba(99, 102, 241, 0.22) !important;
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.35) !important;
            transform: translateY(-1px);
        }

        .stButton > button:disabled {
            opacity: 0.38 !important;
            cursor: not-allowed !important;
            transform: none !important;
        }

        /* Hero Section Styling */
        .utopia-hero {
            text-align: center;
            padding: 2.2rem 1rem 1.3rem 1rem;
            max-width: 820px;
            margin: 0 auto;
        }

        .utopia-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(99, 102, 241, 0.14);
            border: 1px solid rgba(99, 102, 241, 0.4);
            color: #a5b4fc;
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 1rem;
        }

        .utopia-title {
            font-size: clamp(2.3rem, 4.5vw, 3.4rem);
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0 0 0.55rem 0;
            background: linear-gradient(135deg, #ffffff 15%, #a5b4fc 65%, #6366f1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 40px rgba(99, 102, 241, 0.25);
        }

        .utopia-subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
            font-weight: 400;
            margin: 0 auto 1.4rem auto;
            max-width: 660px;
            line-height: 1.5;
        }

        /* Subject Quick-Launch Cards */
        .subject-card {
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.88) 0%, rgba(15, 23, 42, 0.96) 100%);
            border: 1px solid rgba(99, 102, 241, 0.24);
            border-radius: 14px;
            padding: 1.15rem 1.2rem 0.9rem 1.2rem;
            margin-bottom: 0.45rem;
            transition: all 0.22s ease;
            box-shadow: 0 8px 24px rgba(2, 6, 23, 0.45);
        }

        .subject-card:hover {
            border-color: #6366f1;
            box-shadow: 0 0 26px rgba(99, 102, 241, 0.28);
            transform: translateY(-2px);
        }

        .subject-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.45rem;
        }

        .subject-card-title {
            font-size: 1.06rem;
            font-weight: 700;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .subject-card-tag {
            font-size: 0.72rem;
            color: #818cf8;
            background: rgba(99, 102, 241, 0.14);
            border: 1px solid rgba(99, 102, 241, 0.28);
            padding: 2px 8px;
            border-radius: 6px;
        }

        .subject-card-desc {
            font-size: 0.86rem;
            color: #94a3b8;
            line-height: 1.45;
            min-height: 2.5rem;
        }

        /* Status Pills in Top Browser Bar */
        .status-pill-on {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            background: rgba(16, 185, 129, 0.14);
            border: 1px solid rgba(16, 185, 129, 0.45);
            color: #34d399;
            border-radius: 8px;
            padding: 0.36rem 0.6rem;
            font-size: 0.8rem;
            font-weight: 600;
            width: 100%;
            text-align: center;
        }

        .status-pill-off {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            background: rgba(244, 63, 94, 0.14);
            border: 1px solid rgba(244, 63, 94, 0.4);
            color: #fb7185;
            border-radius: 8px;
            padding: 0.36rem 0.6rem;
            font-size: 0.8rem;
            font-weight: 600;
            width: 100%;
            text-align: center;
        }

        /* Full-bleed Web Viewer Frame Border */
        iframe[title="st.iframe"] {
            border: 1px solid rgba(99, 102, 241, 0.32) !important;
            border-radius: 12px !important;
            background-color: #ffffff !important;
            box-shadow: 0 12px 36px rgba(2, 6, 23, 0.65) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_panic_hotkey_engine() -> None:
    """
    Inject a zero-latency DOM decoy screen into window.parent.document so pressing
    Escape or ~ (either on the main app OR inside the web viewer iframe) switches
    the display to a realistic Wikipedia article in <5ms and updates the tab title.
    """
    escaped_decoy = (
        DECOY_WIKIPEDIA_HTML.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    components.html(
        f"""
        <script>
        (function() {{
          try {{
            const parentWin = window.parent;
            const parentDoc = parentWin.document;
            const ORIGINAL_TITLE = "Utopia Education";
            const DECOY_TITLE = "George Washington - Wikipedia";

            let overlay = parentDoc.getElementById("utopia-instant-panic-overlay");
            if (!overlay) {{
              overlay = parentDoc.createElement("div");
              overlay.id = "utopia-instant-panic-overlay";
              overlay.style.cssText = "position:fixed;inset:0;z-index:2147483647;display:none;overflow-y:auto;background:#ffffff;";
              overlay.innerHTML = `{escaped_decoy}`;
              parentDoc.body.appendChild(overlay);
            }}

            parentWin.__utopiaPanicState = parentWin.__utopiaPanicState || false;

            parentWin.__utopiaTogglePanic = function(forceState) {{
              const nextState = typeof forceState === "boolean" ? forceState : !parentWin.__utopiaPanicState;
              parentWin.__utopiaPanicState = nextState;
              if (nextState) {{
                overlay.style.display = "block";
                parentDoc.title = DECOY_TITLE;
              }} else {{
                overlay.style.display = "none";
                parentDoc.title = ORIGINAL_TITLE;
              }}
            }};

            parentWin.utopiaRestore = function() {{
              parentWin.__utopiaTogglePanic(false);
            }};

            if (!parentWin.__utopiaKeyListenerAttached) {{
              parentWin.__utopiaKeyListenerAttached = true;
              parentDoc.addEventListener("keydown", function(e) {{
                if (e.key === "Escape" || e.key === "~" || e.key === "`") {{
                  e.preventDefault();
                  e.stopPropagation();
                  parentWin.__utopiaTogglePanic();
                }}
              }}, true);
            }}
          }} catch (err) {{
            console.warn("Panic overlay initialization notice:", err);
          }}
        }})();
        </script>
        """,
        height=0,
        width=0,
    )


# -----------------------------------------------------------------------------
# 6. UI RENDERERS (DECOY SCREEN, BROWSER BAR, HOME PORTAL, WEB VIEWER)
# -----------------------------------------------------------------------------
def render_panic_decoy_view() -> None:
    """Render full-screen decoy article if triggered via the Streamlit Hide button."""
    components.html(
        """
        <script>
        try { window.parent.document.title = "George Washington - Wikipedia"; } catch(e) {}
        </script>
        """,
        height=0,
    )
    st.markdown(DECOY_WIKIPEDIA_HTML, unsafe_allow_html=True)
    _, right_col = st.columns([9, 1])
    with right_col:
        if st.button("Restore", key="restore_from_panic", help="Return to Utopia Education"):
            st.session_state.panic_active = False
            st.rerun()


def render_top_browser_bar(blocked_count: int, active_mode: str) -> None:
    """Render the sleek, slim top browser bar above the web viewport."""
    can_back = st.session_state.history_index > 0
    can_forward = st.session_state.history_index < len(st.session_state.history) - 1

    c_back, c_fwd, c_rel, c_home, c_url, c_shield, c_toggle, c_mode, c_hide = st.columns(
        [0.45, 0.45, 0.45, 0.55, 5.2, 1.15, 0.75, 0.85, 0.75],
        vertical_alignment="center",
    )

    with c_back:
        if st.button("←", key="nav_back", disabled=not can_back, help="Back", use_container_width=True):
            go_back()
            st.rerun()

    with c_fwd:
        if st.button("→", key="nav_fwd", disabled=not can_forward, help="Forward", use_container_width=True):
            go_forward()
            st.rerun()

    with c_rel:
        if st.button("↻", key="nav_reload", help="Reload Page", use_container_width=True):
            st.session_state.reload_nonce += 1
            st.rerun()

    with c_home:
        if st.button("⌂", key="nav_home", help="Utopia Home", use_container_width=True):
            go_home()
            st.rerun()

    with c_url:
        with st.form("browser_address_form", clear_on_submit=False, border=False):
            url_input = st.text_input(
                "Address Bar",
                value=st.session_state.current_url,
                placeholder="Enter URL or search topic (e.g., khanacademy.org or cellular respiration)...",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Go", use_container_width=False)
            # Hide submit button visually so Enter key submits cleanly
            st.markdown(
                """
                <style>
                div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] {
                    display: none !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            if submitted and url_input.strip():
                navigate_to(url_input, push_history=True)
                st.rerun()

    with c_shield:
        if st.session_state.adblock_enabled:
            st.markdown(
                f'<div class="status-pill-on" title="Ads & Trackers Blocked on this page">🛡️ {blocked_count} Blocked</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="status-pill-off" title="Ad Blocker Disabled">🛡️ Off</div>',
                unsafe_allow_html=True,
            )

    with c_toggle:
        toggle_label = "Shield: ON" if st.session_state.adblock_enabled else "Shield: OFF"
        if st.button(toggle_label, key="toggle_adblock", help="Toggle Built-in Ad & Tracker Blocker", use_container_width=True):
            st.session_state.adblock_enabled = not st.session_state.adblock_enabled
            st.rerun()

    with c_mode:
        mode_label = "Clean View" if active_mode == "proxy" else "Frame View"
        if st.button(mode_label, key="toggle_render_mode", help="Switch between Ad-Cleaned Proxy & Direct Frame", use_container_width=True):
            st.session_state.render_mode = (
                "iframe" if st.session_state.render_mode == "proxy" else "proxy"
            )
            st.rerun()

    with c_hide:
        if st.button("👁️ Hide", key="panic_hide_browser", help="Instant Panic Hide (or press Esc / ~)", use_container_width=True):
            st.session_state.panic_active = True
            st.rerun()


def render_home_screen() -> None:
    """Render the Utopia Education Hero Home Screen and 3-column Subject Quick-Launch Cards."""
    # Top utility bar with Shield status and Panic Hide button
    top_left, top_mid, top_right = st.columns([6.5, 1.5, 1.0], vertical_alignment="center")
    with top_left:
        st.markdown(
            '<div style="font-weight:700;font-size:1.05rem;color:#e2e8f0;padding-left:4px;">📚 Utopia Education</div>',
            unsafe_allow_html=True,
        )
    with top_mid:
        shield_text = "🛡️ Ad & Tracker Blocker: Active" if st.session_state.adblock_enabled else "🛡️ Ad Blocker: Off"
        pill_cls = "status-pill-on" if st.session_state.adblock_enabled else "status-pill-off"
        st.markdown(f'<div class="{pill_cls}">{shield_text}</div>', unsafe_allow_html=True)
    with top_right:
        if st.button("👁️ Hide [Esc]", key="panic_hide_home", use_container_width=True):
            st.session_state.panic_active = True
            st.rerun()

    # Hero Section
    st.markdown(
        """
        <div class="utopia-hero">
            <div class="utopia-badge">✨ Ad-Free Academic Browser &bull; Instant Esc / ~ Quick-Hide</div>
            <h1 class="utopia-title">Utopia Education</h1>
            <p class="utopia-subtitle">
                Schoolwork: ELA, Science, History, Math, Literature, Social Studies, and Writing
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered Glowing Search / URL Bar
    _, search_col, _ = st.columns([1.4, 4.2, 1.4])
    with search_col:
        with st.form("hero_search_form", clear_on_submit=False, border=False):
            in_col, btn_col = st.columns([5.2, 1.1], vertical_alignment="center")
            with in_col:
                hero_query = st.text_input(
                    "Search or Enter URL",
                    placeholder="Search any school topic or enter a website URL (e.g., khanacademy.org)...",
                    label_visibility="collapsed",
                )
            with btn_col:
                hero_submit = st.form_submit_button("Launch →", use_container_width=True)

            if hero_submit and hero_query.strip():
                navigate_to(hero_query, push_history=True)
                st.rerun()

    st.markdown("<div style='height: 1.4rem;'></div>", unsafe_allow_html=True)

    # 3-Column Grid of Subject Quick-Launch Cards
    _, grid_container, _ = st.columns([0.6, 8.8, 0.6])
    with grid_container:
        for row_start in range(0, len(SUBJECT_CARDS), 3):
            cols = st.columns(3, gap="medium")
            for col_idx, card in enumerate(SUBJECT_CARDS[row_start : row_start + 3]):
                with cols[col_idx]:
                    st.markdown(
                        f"""
                        <div class="subject-card">
                            <div class="subject-card-header">
                                <div class="subject-card-title">
                                    <span>{card['icon']}</span>
                                    <span>{card['title']}</span>
                                </div>
                                <span class="subject-card-tag">{card['tag']}</span>
                            </div>
                            <div class="subject-card-desc">{card['desc']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(
                        f"Open {card['title']} →",
                        key=f"launch_card_{row_start + col_idx}",
                        use_container_width=True,
                    ):
                        navigate_to(card["url"], push_history=True)
                        st.rerun()


def render_web_viewer() -> None:
    """Render the built-in ultra-smooth interactive web viewer with Ad Blocker."""
    target_url = st.session_state.current_url

    if st.session_state.render_mode == "iframe":
        page_data = {
            "mode": "iframe",
            "url": target_url,
            "blocked_count": 0,
            "title": target_url,
        }
    else:
        page_data = fetch_and_clean_page(
            target_url,
            st.session_state.adblock_enabled,
            st.session_state.reload_nonce,
        )

    active_mode = str(page_data.get("mode", "proxy"))
    blocked_count = int(page_data.get("blocked_count", 0))

    render_top_browser_bar(blocked_count=blocked_count, active_mode=active_mode)

    if active_mode == "proxy" and page_data.get("html"):
        components.html(
            str(page_data["html"]),
            height=850,
            scrolling=True,
        )
    else:
        safe_iframe_url = html.escape(str(page_data.get("url", target_url)), quote=True)
        fallback_frame_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8" />
          <style>
            html, body {{
              margin: 0;
              padding: 0;
              width: 100%;
              height: 100%;
              overflow: hidden;
              background: #0f172a;
            }}
            iframe {{
              width: 100%;
              height: 850px;
              border: none;
              display: block;
              background: #ffffff;
            }}
          </style>
          <script>
            window.addEventListener("keydown", function(e) {{
              if (e.key === "Escape" || e.key === "~" || e.key === "`") {{
                e.preventDefault();
                try {{
                  if (window.parent && typeof window.parent.__utopiaTogglePanic === "function") {{
                    window.parent.__utopiaTogglePanic(true);
                  }}
                }} catch (err) {{}}
              }}
            }}, true);
          </script>
        </head>
        <body>
          <iframe
            src="{safe_iframe_url}"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
            allowfullscreen
            loading="eager"
          ></iframe>
        </body>
        </html>
        """
        components.html(
            fallback_frame_html,
            height=850,
            scrolling=False,
        )


# -----------------------------------------------------------------------------
# 7. MAIN APPLICATION ENTRYPOINT
# -----------------------------------------------------------------------------
def main() -> None:
    init_session_state()
    handle_query_param_navigation()
    inject_global_styles()
    inject_panic_hotkey_engine()

    if st.session_state.panic_active:
        render_panic_decoy_view()
    elif st.session_state.view_mode == "browser" and st.session_state.current_url:
        render_web_viewer()
    else:
        render_home_screen()


if __name__ == "__main__":
    main()
