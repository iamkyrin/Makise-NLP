import html
import streamlit as st
from summarizer import summarize
from classifier import classify_document
from extractor import extract_entities
import pdfplumber
from exporter import export_summary

st.set_page_config(page_title="Makise", layout="wide", page_icon="▪")
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #ffffff !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #1a1a1a !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] * { color: #ffffff !important; }
[data-testid="stSidebarContent"] { padding: 2rem 1.5rem !important; }

footer { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; border: none !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.block-container { max-width: 780px; margin: 0 auto; padding: 2rem 1.5rem 8rem !important; }

/* Radio Content */
/* hide the circle */
label[data-baseweb="radio"] > div:first-child { display: none; }

label[data-baseweb="radio"] {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #e0e0e0;
    padding: 8px 16px;
    border-radius: 15px;
    cursor: pointer;
    font-size: 0.78rem;
    transition: all 0.15s ease;
}

label[data-baseweb="radio"] p { color: #0a0a0a !important; }

label[data-baseweb="radio"]:has(input:checked) {
    background-color: #f54e4e !important;
    border-color: #f54e4e !important;
}

label[data-baseweb="radio"]:has(input:checked) p { color: #ffffff !important; }

[data-testid="stRadio"] {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
}
/* Sidebar content */
.sidebar-logo { font-size: 1.2rem; font-weight: 600; color: #ffffff; letter-spacing: -0.5px; margin-bottom: 0.25rem; }
.sidebar-tagline { font-size: 0.75rem; color: #555555; font-weight: 300; margin-bottom: 2.5rem; }
.sidebar-section { font-size: 0.65rem; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; color: #444444; margin-bottom: 0.75rem; }
.sidebar-item { display: flex; align-items: center; gap: 0.6rem; padding: 0.5rem 0.75rem; border-radius: 6px; font-size: 0.82rem; font-weight: 400; color: #cccccc; margin-bottom: 0.25rem; }
.sidebar-item.active { background: #1a1a1a; color: #ffffff; }
.sidebar-dot { width: 6px; height: 6px; border-radius: 50%; background: #333333; flex-shrink: 0; display: inline-block; }
.sidebar-dot.green { background: #4ade80; }
.sidebar-divider { height: 1px; background: #1a1a1a; margin: 1.5rem 0; }

/* Sidebar Streamlit components */
[data-testid="stSidebar"] label { color: #666666 !important; font-size: 0.65rem !important; font-weight: 500 !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; margin-bottom: 0.5rem !important; }
[data-testid="stSidebar"] p { color: #cccccc !important; font-size: 0.82rem !important; }

/* Sidebar radio */
[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child { display: none !important; }
[data-testid="stSidebar"] label[data-baseweb="radio"] { border: 1px solid #2a2a2a !important; border-radius: 8px !important; padding: 6px 12px !important; margin-bottom: 4px !important; cursor: pointer !important; }
[data-testid="stSidebar"] label[data-baseweb="radio"] p { color: #aaaaaa !important; font-size: 0.78rem !important; letter-spacing: 0 !important; text-transform: none !important; }
[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) { background: #1a1a1a !important; border-color: #f54e4e !important; }
[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p { color: #ffffff !important; }

/* Sidebar selectbox */
[data-testid="stSidebar"] [data-testid="stSelectbox"] { margin-top: 0.5rem; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div { background: #1a1a1a !important; border: 1px solid #2a2a2a !important; border-radius: 8px !important; color: #cccccc !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg { fill: #666666 !important; }

/* Sidebar download button */
[data-testid="stDownloadButton"] button {
    background: #1a1a1a !important;
    border: 1px solid #2a2a2a !important;
    color: #cccccc !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-size: 0.78rem !important;
    padding: 0.5rem 1rem !important; 
}
[data-testid="stDownloadButton"] button:hover { border-color: #f54e4e !important; color: #ffffff !important; }    
/* Chat messages */
.chat-wrap { display: flex; flex-direction: column; gap: 1.5rem; padding-bottom: 1rem; }

.msg-user {
    display: flex;
    justify-content: flex-end;
}
.msg-user-bubble {
    background: #0a0a0a;
    color: #ffffff;
    border-radius: 16px 16px 4px 16px;
    padding: 0.85rem 1.1rem;
    max-width: 80%;
    font-size: 0.875rem;
    line-height: 1.6;
    font-weight: 300;
    font-family: 'JetBrains Mono', monospace;
    white-space: pre-wrap;
    word-break: break-word;
}

.msg-system {
    display: flex;
    justify-content: flex-start;
    flex-direction: column;
    gap: 0.75rem;
}
.msg-system-label {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #aaaaaa;
    padding-left: 0.25rem;
}

/* Result rows */
.result-row {
    background: #f9f9f9;
    border: 1px solid #eeeeee;
    border-radius: 12px;
    padding: 1rem 1.25rem;
}
.result-tag {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #999999;
    margin-bottom: 0.4rem;
}
.result-value {
    font-size: 0.9rem;
    font-weight: 500;
    color: #0a0a0a;
    line-height: 1.6;
}
.result-value.mono {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 300;
    font-size: 0.85rem;
    color: #333333;
}

/* Entity pills */
.entity-wrap { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.25rem; }
.entity-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 100px;
    padding: 0.15rem 0.65rem;
    font-size: 0.72rem;
    color: #0a0a0a;
    font-family: 'Inter', sans-serif;
}
.entity-pill-type {
    font-size: 0.6rem;
    color: #999999;
    font-weight: 500;
}
.entity-pill.more {
    color: #999999;
    border-style: dashed;
}

/* Welcome state */
.welcome-wrap {
    text-align: center;
    padding: 4rem 2rem;
    color: #cccccc;
}
.welcome-title {
    font-size: 1.5rem;
    font-weight: 500;
    color: #0a0a0a;
    margin-bottom: 0.5rem;
}
.welcome-sub {
    font-size: 0.875rem;
    color: #888888;
    font-weight: 300;
    margin-bottom: 2.5rem;
}
.welcome-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }
.welcome-chip {
    background: #f4f4f4;
    border: 1px solid #e8e8e8;
    border-radius: 100px;
    padding: 0.4rem 1rem;
    font-size: 0.78rem;
    color: #555555;
}

/* Input bar */
.input-bar-wrap {
    position: fixed;
    bottom: 0; left: 260px; right: 0;
    background: #ffffff;
    border-top: 1px solid #eeeeee;
    padding: 1rem 2rem;
    z-index: 100;
}

[data-testid="stTextArea"] textarea {
    background: #f7f7f7 !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 12px !important;
    color: #0a0a0a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 300 !important;
    line-height: 1.6 !important;
    padding: 0.85rem 1rem !important;
    resize: none !important;
    transition: border-color 0.15s ease !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #0a0a0a !important;
    background: #ffffff !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

[data-testid="stButton"] button {
    background: #0a0a0a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: background 0.15s ease !important;
    white-space: nowrap !important;
}
[data-testid="stButton"] button:hover { background: #222222 !important; }

[data-testid="stSpinner"] { color: #0a0a0a !important; }
[data-testid="stColumns"] { gap: 0.75rem !important; align-items: flex-end !important; }
[data-testid="column"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">Makise</div>
    <div class="sidebar-tagline">Document Intelligence Pipeline</div>
    <div class="sidebar-section">Tools</div>
    <div class="sidebar-item active"><span class="sidebar-dot green"></span> Analyze</div>
    <div class="sidebar-divider"></div>
    <div class="sidebar-section">Models</div>
    <div class="sidebar-item"><span class="sidebar-dot"></span> Classifier</div>
    <div class="sidebar-item"><span class="sidebar-dot"></span> NER · spaCy</div>
    <div class="sidebar-item"><span class="sidebar-dot"></span> BART · CNN</div>
    <div class="sidebar-divider"></div>
    <div class="sidebar-section">Settings</div>
    """, unsafe_allow_html=True)

    radio = st.select_slider(label="Summary Length", options=["Short", "Medium", "Detailed"])
    select_box = st.selectbox(label="Language", options=["English", "French", "Spanish"])

    st.markdown("""
    <div class="sidebar-divider"></div>
    <div class="sidebar-section">About</div>
    <div class="sidebar-item"><span class="sidebar-dot"></span> NLP Pipeline v1.2.0-alpha</div>
    """, unsafe_allow_html=True)
# ── Init session state ────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Chat history ──────────────────────────────────────────────────────────────
PILL_LIMIT = 20

if not st.session_state.history:
    st.markdown("""
    <div class="welcome-wrap">
        <div class="welcome-title">What would you like to analyze?</div>
        <div class="welcome-sub">Paste any document below to classify, extract entities, and summarize.</div>
        <div class="welcome-chips">
            <span class="welcome-chip">News articles</span>
            <span class="welcome-chip">Research papers</span>
            <span class="welcome-chip">Legal documents</span>
            <span class="welcome-chip">Business reports</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for entry in st.session_state.history:
        # User message
        preview = entry["text"][:300] + "\u2026" if len(entry["text"]) > 300 else entry["text"]
        st.markdown(f"""
        <div class="msg-user">
            <div class="msg-user-bubble">{html.escape(preview)}</div>
        </div>
        """, unsafe_allow_html=True)

        # System result
        seen = {}
        for k, v in entry["entities"].items():
            base = k.rsplit('_', 1)[0] if '_' in k else k
            if base not in seen:
                seen[base] = v

        all_items = list(seen.items())
        visible = all_items[:PILL_LIMIT]
        overflow = len(all_items) - PILL_LIMIT

        pills = "".join([
            f'<div class="entity-pill">{html.escape(name)} <span class="entity-pill-type">{html.escape(label)}</span></div>'
            for name, label in visible
        ])
        if overflow > 0:
            pills += f'<div class="entity-pill more">+{overflow} more</div>'

        st.markdown(f"""
        <div class="msg-system">
            <div class="msg-system-label">Makise · Analysis</div>
            <div class="result-row">
                <div class="result-tag">Classification</div>
                <div class="result-value">{html.escape(entry["classification"])}</div>
            </div>
            <div class="result-row">
                <div class="result-tag">Named Entities</div>
                <div class="entity-wrap">{pills}</div>
            </div>
            <div class="result-row">
                <div class="result-tag">Summary</div>
                <div class="result-value mono">{html.escape(entry["summary"])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)  # spacer
    st.markdown('</div>', unsafe_allow_html=True)

# ── Input bar ─────────────────────────────────────────────────────────────────
if st.session_state.history and "summary" in st.session_state.history[-1]:
    st.download_button(
        label="Export Summary",
        data=export_summary(st.session_state.history[-1]["summary"]),
        file_name="summary.pdf"
    )
    st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
st.markdown('<div style="height: 120px" class="input-bar-wrap">', unsafe_allow_html=True)
col1, col2 = st.columns([6,1])
with col1:
    text_input = st.text_area(" ", height=68, placeholder="Paste a document to analyze…")
    file_upload = st.file_uploader(" ", type=["pdf", "txt"], accept_multiple_files=True)
with col2:
    run = st.button("Analyze →")
st.markdown('</div>', unsafe_allow_html=True)

if run:
    if select_box != "English":
        st.toast("Multi-language support coming soon...")
    else:
        if file_upload:
            for file in file_upload:
                all_text = ""
                if file.name.endswith(".pdf"):
                    try:
                        with st.spinner("Running pipeline…"):
                            with pdfplumber.open(file) as pdf:
                                for page in pdf.pages:
                                    text = page.extract_text()
                                    if text:
                                        all_text += text + "\\n"

                            classification = classify_document(all_text)
                            entities = extract_entities(all_text)
                            summary = summarize(all_text, radio)
                        st.session_state.history.append({
                            "text": all_text,
                            "classification": classification,
                            "entities": entities,
                            "summary": summary,
                        })

                    except Exception as e:
                        st.toast(f"Pipeline error: {e}")

                elif file.name.endswith(".txt"):
                    try:
                        with st.spinner("Running pipeline…"):
                            text = file.read().decode("utf-8")
                            all_text += text + "\\n"

                            classification = classify_document(all_text)
                            entities = extract_entities(all_text)
                            summary = summarize(all_text, radio)
                        st.session_state.history.append({
                            "text": all_text,
                            "classification": classification,
                            "entities": entities,
                            "summary": summary,
                        })
                    except Exception as e:
                        st.toast(f"Pipeline error: {e}")
            st.rerun()
        elif not text_input.strip():
            st.toast("Paste a document first.", icon="⚠️")
        else:
            try:
                with st.spinner("Running pipeline…"):
                    classification = classify_document(text_input)
                    entities = extract_entities(text_input)
                    summary = summarize(text_input, radio)
                st.session_state.history.append({
                    "text": text_input,
                    "classification": classification,
                    "entities": entities,
                    "summary": summary,
                })
                st.rerun()
            except Exception as e:
                st.toast(f"Pipeline error: {e}")
