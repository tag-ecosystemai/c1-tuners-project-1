import base64
import os
import tempfile
from datetime import datetime
from io import BytesIO

import streamlit as st
from PIL import Image

from ai.inference.predict import predict

# --------------------------------------------------------------------------
# Page config — must be the first Streamlit call
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Verdict — Potato Leaf Inspector",
    page_icon="🥔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------
# Design system — CSS (dark, agritech, product-grade)
# --------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #0a120c;
        --bg-elev: #0e1811;
        --panel: #101c14;
        --panel-2: #0c1610;
        --border: rgba(255,255,255,0.08);
        --border-strong: rgba(255,255,255,0.16);
        --text: #eef3ee;
        --text-muted: #93a89b;
        --text-faint: #63776a;
        --accent: #e2953f;
        --accent-strong: #c97f2f;
        --accent-soft: rgba(226, 149, 63, 0.14);
        --success: #34d399;
        --success-soft: rgba(52, 211, 153, 0.12);
        --danger: #f87171;
        --danger-soft: rgba(248, 113, 113, 0.12);
    }

    html, body, [class*="css"] { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] { background: transparent; }

    .stApp, [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1220px; }
    p, span, div { color: var(--text); }

    /* ================= Sidebar ================= */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #08100b 0%, #0a140d 100%);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

    .brand-wrap { display: flex; align-items: center; gap: 0.55rem; padding: 0 0.35rem 0.2rem 0.35rem; }
    .brand-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 10px var(--accent); }
    .brand-name { font-weight: 800; letter-spacing: 0.14em; font-size: 0.85rem; color: var(--text); text-transform: uppercase; }
    .brand-tagline { font-size: 0.74rem; color: var(--text-faint); padding: 0.15rem 0.35rem 1.1rem 0.35rem; }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        color: var(--text-muted);
        border: none;
        border-radius: 10px;
        text-align: left;
        justify-content: flex-start;
        box-shadow: none;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.55rem 0.7rem;
        width: 100%;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.05);
        color: var(--text);
    }
    section[data-testid="stSidebar"] .stButton > button:disabled {
        background: var(--accent-soft) !important;
        color: var(--accent) !important;
        opacity: 1 !important;
        border: 1px solid rgba(226,149,63,0.3);
        cursor: default;
    }

    .sidebar-note {
        font-size: 0.74rem;
        color: var(--text-faint);
        line-height: 1.5;
        padding: 0.8rem 0.35rem 0 0.35rem;
        border-top: 1px solid var(--border);
        margin-top: 1rem;
    }

    /* ================= Top bar ================= */
    .topbar-title { font-size: 1.55rem; font-weight: 800; color: var(--text); margin: 0; letter-spacing: -0.01em; }
    .topbar-subtitle { font-size: 0.9rem; color: var(--text-muted); margin-top: 0.15rem; }
    .eyebrow {
        text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.7rem;
        font-weight: 700; color: var(--accent); margin-bottom: 0.3rem;
    }

    /* ================= Buttons (main area = accent) ================= */
    .stButton > button, .stDownloadButton > button {
        background: var(--accent);
        color: #17110a;
        border: none;
        border-radius: 11px;
        padding: 0.68rem 1.2rem;
        font-weight: 700;
        font-size: 0.92rem;
        box-shadow: 0 8px 20px -8px rgba(226,149,63,0.55);
        transition: transform 0.05s ease, box-shadow 0.15s ease, background 0.15s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: var(--accent-strong);
        box-shadow: 0 10px 22px -8px rgba(201,127,47,0.6);
    }
    .stButton > button:active { transform: translateY(1px); }
    button[kind="secondary"] {
        background: transparent !important;
        color: var(--text-muted) !important;
        border: 1px solid var(--border-strong) !important;
        box-shadow: none !important;
    }
    button[kind="secondary"]:hover { color: var(--text) !important; border-color: var(--text-faint) !important; }

    /* ================= Cards / panels ================= */
    .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.1rem;
    }
    .panel-title {
        font-size: 0.95rem; font-weight: 700; color: var(--text);
        margin-bottom: 0.65rem; display: flex; align-items: center; gap: 0.5rem;
    }
    .panel-text { color: var(--text-muted); font-size: 0.87rem; line-height: 1.6; }

    /* ================= Hero (Home) ================= */
    .hero-headline {
        font-size: 2.2rem; font-weight: 800; line-height: 1.15; color: var(--text);
        letter-spacing: -0.02em; margin-bottom: 0.9rem;
    }
    .hero-desc { font-size: 0.98rem; color: var(--text-muted); line-height: 1.7; margin-bottom: 1.6rem; max-width: 34ch; }

    /* ================= Bracket-frame media card ================= */
    .frame-card {
        position: relative;
        border-radius: 20px;
        background: radial-gradient(circle at 50% 30%, #16301f 0%, #0b1710 72%);
        border: 1px solid var(--border);
        display: flex; align-items: center; justify-content: center;
        overflow: hidden;
    }
    .frame-corner { position: absolute; width: 22px; height: 22px; opacity: 0.6; }
    .frame-corner.tl { top: 14px; left: 14px; border-top: 2px solid var(--text); border-left: 2px solid var(--text); border-radius: 5px 0 0 0; }
    .frame-corner.tr { top: 14px; right: 14px; border-top: 2px solid var(--text); border-right: 2px solid var(--text); border-radius: 0 5px 0 0; }
    .frame-corner.bl { bottom: 14px; left: 14px; border-bottom: 2px solid var(--text); border-left: 2px solid var(--text); border-radius: 0 0 0 5px; }
    .frame-corner.br { bottom: 14px; right: 14px; border-bottom: 2px solid var(--text); border-right: 2px solid var(--text); border-radius: 0 0 5px 0; }
    .frame-img { width: 100%; height: 100%; object-fit: cover; position: absolute; inset: 0; }
    .frame-placeholder-icon { font-size: 3.4rem; opacity: 0.35; filter: grayscale(0.3); }
    .frame-status {
        position: absolute; bottom: 16px; left: 16px;
        background: rgba(6, 12, 8, 0.65); backdrop-filter: blur(6px);
        padding: 0.4rem 0.85rem; border-radius: 999px;
        font-size: 0.76rem; font-weight: 600; color: #eaf1ec;
        display: flex; align-items: center; gap: 0.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .frame-status-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 8px var(--accent); }

    /* ================= Recent strip ================= */
    .recent-card {
        background: var(--panel); border: 1px solid var(--border); border-radius: 14px;
        padding: 0.85rem; display: flex; gap: 0.7rem; align-items: center;
    }
    .recent-thumb { width: 46px; height: 46px; border-radius: 10px; object-fit: cover; border: 1px solid var(--border); flex-shrink: 0; }
    .recent-name { font-weight: 700; font-size: 0.82rem; color: var(--text); }
    .recent-meta { font-size: 0.74rem; color: var(--text-faint); }

    /* ================= Upload dropzone ================= */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--panel-2);
        border: 1.5px dashed var(--border-strong);
        border-radius: 14px;
    }
    [data-testid="stFileUploaderDropzone"]:hover { border-color: var(--accent); }
    [data-testid="stFileUploaderDropzone"] small, [data-testid="stFileUploaderDropzone"] span { color: var(--text-muted) !important; }

    /* ================= Status banners ================= */
    .status-banner {
        display: flex; align-items: flex-start; gap: 0.85rem;
        border-radius: 14px; padding: 1rem 1.15rem; margin-bottom: 1.1rem;
        border: 1px solid transparent;
    }
    .status-banner.success { background: var(--success-soft); border-color: rgba(52,211,153,0.3); }
    .status-banner.danger { background: var(--danger-soft); border-color: rgba(248,113,113,0.3); }
    .status-icon { font-size: 1.4rem; line-height: 1; margin-top: 1px; }
    .status-title { font-weight: 800; font-size: 1rem; color: var(--text); margin: 0 0 2px 0; }
    .status-desc { font-size: 0.85rem; color: var(--text-muted); margin: 0; }

    /* ================= Metric tiles ================= */
    .metric-tile {
        background: var(--panel-2); border: 1px solid var(--border); border-radius: 14px;
        padding: 1rem 1.05rem; height: 100%;
    }
    .metric-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 700; color: var(--text-faint); margin-bottom: 0.4rem; }
    .metric-value { font-size: 1.3rem; font-weight: 800; color: var(--text); }

    .pill { display: inline-block; padding: 0.22rem 0.65rem; border-radius: 999px; font-size: 0.76rem; font-weight: 700; }
    .pill-high { background: var(--success-soft); color: var(--success); }
    .pill-medium { background: var(--accent-soft); color: var(--accent); }
    .pill-low { background: var(--danger-soft); color: var(--danger); }

    .conf-bar-track { width: 100%; height: 8px; background: rgba(255,255,255,0.08); border-radius: 999px; overflow: hidden; margin-top: 0.55rem; }
    .conf-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--accent-strong), var(--accent)); }

    .gradcam-placeholder {
        border: 1.5px dashed var(--border-strong); border-radius: 14px; background: var(--panel-2);
        padding: 2rem 1rem; text-align: center; color: var(--text-faint); font-size: 0.84rem;
    }

    /* ================= Gallery grid ================= */
    .gallery-card { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; margin-bottom: 1rem; }
    .gallery-thumb { width: 100%; height: 150px; object-fit: cover; display: block; background: var(--panel-2); }
    .gallery-body { padding: 0.9rem 1rem 1.05rem 1rem; }
    .gallery-name { font-weight: 700; font-size: 0.85rem; color: var(--text); margin-bottom: 0.3rem; }
    .gallery-meta { font-size: 0.76rem; color: var(--text-faint); margin-top: 0.35rem; }

    .empty-state { text-align: center; padding: 3rem 1rem; color: var(--text-muted); }
    .empty-state-icon { font-size: 2.4rem; margin-bottom: 0.6rem; opacity: 0.5; }

    hr.soft-divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
if "view" not in st.session_state:
    st.session_state.view = "home"
if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_image" not in st.session_state:
    st.session_state.last_image = None
if "last_filename" not in st.session_state:
    st.session_state.last_filename = None


# --------------------------------------------------------------------------
# Presentation helpers (no inference logic here)
# --------------------------------------------------------------------------
def pil_to_data_uri(image, max_width: int = 900, quality: int = 85) -> str:
    img = image.copy()
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)))
    buf = BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=quality)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}"


def render_frame_card(image, status_text, height: int = 420, icon: str = "🛡️") -> None:
    media_html = (
        f'<img src="{pil_to_data_uri(image)}" class="frame-img" />'
        if image is not None
        else f'<div class="frame-placeholder-icon">{icon}</div>'
    )
    status_html = (
        f'<div class="frame-status"><span class="frame-status-dot"></span>{status_text}</div>'
        if status_text
        else ""
    )
    st.markdown(
        f"""
        <div class="frame-card" style="min-height:{height}px;">
            <span class="frame-corner tl"></span>
            <span class="frame-corner tr"></span>
            <span class="frame-corner bl"></span>
            <span class="frame-corner br"></span>
            {media_html}
            {status_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def confidence_pill_class(level: str) -> str:
    level_lower = (level or "").strip().lower()
    if level_lower in ("high", "very high"):
        return "pill-high"
    if level_lower in ("medium", "moderate"):
        return "pill-medium"
    return "pill-low"


def add_to_history(filename: str, result: dict, image) -> None:
    thumb = pil_to_data_uri(image, max_width=260, quality=75)
    if not result["is_potato_leaf"]:
        entry = {
            "name": filename,
            "time": datetime.now().strftime("%H:%M:%S"),
            "status": "Not a potato leaf",
            "prediction": "—",
            "confidence": result.get("potato_probability", 0.0),
            "thumb": thumb,
            "ok": False,
        }
    else:
        entry = {
            "name": filename,
            "time": datetime.now().strftime("%H:%M:%S"),
            "status": "Analyzed",
            "prediction": result.get("prediction", "—"),
            "confidence": result.get("confidence", 0.0),
            "thumb": thumb,
            "ok": True,
        }
    st.session_state.history.insert(0, entry)
    st.session_state.history = st.session_state.history[:24]


def run_inference(image) -> dict:
    """Wraps the existing predict() call — inference logic untouched."""
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_path = temp_file.name
            image.save(temp_path, format="JPEG")
        return predict(temp_path)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def go(view: str) -> None:
    st.session_state.view = view
    st.rerun()


def render_topbar(title: str, subtitle: str, cta_label: str = None, cta_view: str = None) -> None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"""
            <p class="topbar-title">{title}</p>
            <p class="topbar-subtitle">{subtitle}</p>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if cta_label:
            st.write("")
            if st.button(cta_label, use_container_width=True, key=f"cta_{cta_view}"):
                go(cta_view)
    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Sidebar — navigation
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-wrap"><span class="brand-dot"></span><span class="brand-name">Verdict</span></div>
        <div class="brand-tagline">Potato leaf health intelligence</div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = [("home", "🏠  Home"), ("inspect", "📷  Inspect"), ("gallery", "▦  Gallery")]
    for view_key, label in nav_items:
        if st.button(label, key=f"nav_{view_key}", disabled=(st.session_state.view == view_key)):
            go(view_key)

    st.markdown(
        f"""
        <div class="sidebar-note">
            {len(st.session_state.history)} inspection(s) this session.<br><br>
            Built for research &amp; field-support use. Not a substitute for expert agronomic advice.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================================
# HOME
# ==========================================================================
if st.session_state.view == "home":
    hour = datetime.now().hour
    greeting = "Good morning." if hour < 12 else "Good afternoon." if hour < 18 else "Good evening."
    render_topbar(greeting, "Here's what's been happening with your crops.", "＋ New inspection", "inspect")

    hero_left, hero_right = st.columns([1, 1.1], gap="large")

    with hero_left:
        st.markdown("<div class='eyebrow'>AI Crop Health</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-headline'>See what's growing wrong, before it spreads.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='hero-desc'>Photograph a potato leaf and get an instant read on its "
            "condition — with a confidence score, not just a guess.</div>",
            unsafe_allow_html=True,
        )
        if st.button("📷  Inspect a crop"):
            go("inspect")

    with hero_right:
        if st.session_state.last_image is not None and st.session_state.last_result is not None:
            r = st.session_state.last_result
            status = ("Potato leaf · " + r["prediction"]) if r["is_potato_leaf"] else "Not a potato leaf"
            render_frame_card(st.session_state.last_image, status, height=380)
        else:
            render_frame_card(None, "Ready when you are", height=380)

    if st.session_state.history:
        st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>Recent activity</div>", unsafe_allow_html=True)
        recent = st.session_state.history[:3]
        cols = st.columns(len(recent))
        for col, item in zip(cols, recent):
            with col:
                st.markdown(
                    f"""
                    <div class="recent-card">
                        <img class="recent-thumb" src="{item['thumb']}" />
                        <div>
                            <div class="recent-name">{item['name'][:20]}</div>
                            <div class="recent-meta">{item['status']} · {item['time']}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ==========================================================================
# INSPECT
# ==========================================================================
elif st.session_state.view == "inspect":
    render_topbar("Inspect a crop", "Upload a leaf photo to verify it's a potato leaf and screen for disease.")

    left_col, right_col = st.columns([1, 1.2], gap="large")

    with left_col:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
        )
        st.markdown(
            "<div class='panel-text'>Best results with a single, well-lit leaf against a plain "
            "background. Supported formats: JPG, JPEG, PNG, WEBP.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        image = None
        analyze_clicked = False
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert("RGB")
            render_frame_card(image, "Ready to analyze", height=320)
            st.markdown("<div style='height:0.9rem'></div>", unsafe_allow_html=True)
            analyze_clicked = st.button("🔍  Analyze Image", use_container_width=True)
        else:
            render_frame_card(None, None, height=320, icon="📷")

    with right_col:
        if uploaded_file is not None and analyze_clicked:
            with st.spinner("Analyzing image..."):
                result = run_inference(image)
            st.session_state.last_result = result
            st.session_state.last_image = image
            st.session_state.last_filename = uploaded_file.name
            add_to_history(uploaded_file.name, result, image)

        result = st.session_state.last_result

        if result is None:
            st.markdown(
                "<div class='panel'><div class='panel-text'>"
                "Upload an image and click <strong>Analyze Image</strong> to see the leaf status, "
                "disease prediction, confidence, and recommendations here."
                "</div></div>",
                unsafe_allow_html=True,
            )
        elif not result["is_potato_leaf"]:
            st.markdown(
                f"""
                <div class="status-banner danger">
                    <div class="status-icon">⚠️</div>
                    <div>
                        <p class="status-title">Not a potato leaf</p>
                        <p class="status-desc">
                            The uploaded image does not appear to show a potato leaf.
                            Potato-leaf probability: <strong>{result['potato_probability']:.2%}</strong>
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>💡 Recommendation</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panel-text'>{result['recommendation']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="status-banner success">
                    <div class="status-icon">✅</div>
                    <div>
                        <p class="status-title">Potato leaf detected</p>
                        <p class="status-desc">The image was successfully identified as a potato leaf.</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(
                    f"""<div class="metric-tile"><div class="metric-label">Disease</div>
                    <div class="metric-value">{result['prediction']}</div></div>""",
                    unsafe_allow_html=True,
                )
            with m2:
                pct = max(0, min(100, result["confidence"] * 100))
                st.markdown(
                    f"""<div class="metric-tile"><div class="metric-label">Confidence</div>
                    <div class="metric-value">{result['confidence']:.1%}</div>
                    <div class="conf-bar-track"><div class="conf-bar-fill" style="width:{pct:.1f}%;"></div></div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with m3:
                pill_class = confidence_pill_class(result.get("confidence_level", ""))
                st.markdown(
                    f"""<div class="metric-tile"><div class="metric-label">Confidence level</div>
                    <span class="pill {pill_class}">{result['confidence_level']}</span></div>""",
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>🧠 Explanation</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panel-text'>{result['explanation']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>💡 Recommendation</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='panel-text'>{result['recommendation']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='panel'>", unsafe_allow_html=True)
            st.markdown("<div class='panel-title'>🔬 Model attention (Grad-CAM)</div>", unsafe_allow_html=True)
            st.markdown(
                """<div class="gradcam-placeholder">Grad-CAM heatmap visualization will appear here in a
                future update, highlighting the regions of the leaf that most influenced this prediction.</div>""",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================================
# GALLERY
# ==========================================================================
elif st.session_state.view == "gallery":
    render_topbar(
        "Inspection gallery",
        "Every inspection you've run this session, in one place.",
        "＋ New inspection",
        "inspect",
    )

    if not st.session_state.history:
        st.markdown(
            """
            <div class="panel empty-state">
                <div class="empty-state-icon">🗂️</div>
                <div style="font-weight:700; color:var(--text); margin-bottom:0.3rem;">No inspections yet</div>
                <div class="panel-text">Run your first inspection and it will show up here.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        history = st.session_state.history
        n_cols = 3
        for row_start in range(0, len(history), n_cols):
            row_items = history[row_start:row_start + n_cols]
            cols = st.columns(n_cols)
            for col, item in zip(cols, row_items):
                with col:
                    pill_class = "pill-high" if item["ok"] else "pill-low"
                    st.markdown(
                        f"""
                        <div class="gallery-card">
                            <img class="gallery-thumb" src="{item['thumb']}" />
                            <div class="gallery-body">
                                <div class="gallery-name">{item['name'][:26]}</div>
                                <span class="pill {pill_class}">{item['status']}</span>
                                <div class="gallery-meta">{item['prediction']} · {item['confidence']:.1%} · {item['time']}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
        if st.button("Clear history", type="secondary"):
            st.session_state.history = []
            st.session_state.last_result = None
            st.session_state.last_image = None
            st.session_state.last_filename = None
            st.rerun()