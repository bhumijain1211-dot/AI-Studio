import streamlit as st
from backend import chat, summarize, generate_content, MODELS

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state defaults ────────────────────────────────────────────────────
if "dark_mode"     not in st.session_state: st.session_state.dark_mode     = True
if "tool"          not in st.session_state: st.session_state.tool          = "💬 Chat"
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "chat_input_val" not in st.session_state: st.session_state.chat_input_val = ""
if "sum_result"    not in st.session_state: st.session_state.sum_result    = ""
if "gen_result"    not in st.session_state: st.session_state.gen_result    = ""

# ── Theme colours ─────────────────────────────────────────────────────────────
dark = st.session_state.dark_mode
if dark:
    BG, SURFACE, BORDER = "#0f0f0f", "#1a1a1a", "#2e2e2e"
    TEXT, SUBTEXT        = "#f0f0f0", "#888888"
    BTN_BG, BTN_TEXT     = "#ffffff", "#000000"
    ACTIVE_BG            = "#2a2a2a"
else:
    BG, SURFACE, BORDER  = "#f5f5f5", "#ffffff", "#e0e0e0"
    TEXT, SUBTEXT        = "#111111", "#666666"
    BTN_BG, BTN_TEXT     = "#111111", "#ffffff"
    ACTIVE_BG            = "#e8e8e8"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {{
    background: {BG} !important;
    color: {TEXT} !important;
    font-family: 'Sora', sans-serif !important;
}}

/* ── Sidebar always visible ── */
[data-testid="stSidebar"] {{
    background: {SURFACE} !important;
    border-right: 1px solid {BORDER} !important;
    min-width: 220px !important;
}}
/* Force sidebar text visible */
[data-testid="stSidebar"],
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {{
    color: {TEXT} !important;
}}

/* Hide collapse arrow so sidebar is always visible */
[data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* ── All buttons base style ── */
.stButton > button {{
    background: transparent !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 400 !important;
    width: 100% !important;
    text-align: left !important;
    padding: 0.5rem 0.9rem !important;
    transition: background 0.15s, border-color 0.15s !important;
    margin-bottom: 4px !important;
}}
.stButton > button:hover {{
    background: {ACTIVE_BG} !important;
    border-color: {TEXT} !important;
}}

/* Active tool highlight */
.active-tool > button {{
    background: {BTN_BG} !important;
    color: {BTN_TEXT} !important;
    border-color: {BTN_BG} !important;
    font-weight: 600 !important;
}}

/* Send / action buttons */
.action-btn > button {{
    background: {BTN_BG} !important;
    color: {BTN_TEXT} !important;
    border: none !important;
    font-weight: 500 !important;
    text-align: center !important;
    width: auto !important;
}}

/* ── Inputs ── */
textarea, input[type="text"] {{
    background: {SURFACE} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
}}
textarea:focus, input[type="text"]:focus {{
    border-color: {BTN_BG} !important;
    box-shadow: 0 0 0 2px {'#ffffff33' if dark else '#00000022'} !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {{
    background: {SURFACE} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
}}

/* ── Output card ── */
.output-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    color: {TEXT};
    line-height: 1.75;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-size: 0.95rem;
    margin-top: 1rem;
}}

/* ── Chat bubbles ── */
.bubble-user {{
    background: {BTN_BG};
    color: {BTN_TEXT};
    border-radius: 18px 18px 4px 18px;
    padding: 0.7rem 1rem;
    max-width: 75%;
    margin-left: auto;
    margin-bottom: 6px;
    font-size: 0.93rem;
    line-height: 1.5;
}}
.bubble-ai {{
    background: {SURFACE};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 18px 18px 18px 4px;
    padding: 0.7rem 1rem;
    max-width: 75%;
    margin-bottom: 6px;
    font-size: 0.93rem;
    line-height: 1.5;
}}

/* ── Section headings ── */
.section-title {{
    font-size: 1.5rem;
    font-weight: 600;
    color: {TEXT};
    margin-bottom: 0.2rem;
}}
.section-sub {{
    font-size: 0.88rem;
    color: {SUBTEXT};
    margin-bottom: 1.4rem;
}}

/* ── Divider ── */
hr {{ border: none; border-top: 1px solid {BORDER} !important; margin: 0.9rem 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-thumb {{ background: {BORDER}; border-radius: 10px; }}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<h2 style='font-size:1.3rem;font-weight:600;margin-bottom:2px;color:{TEXT}'>✦ AI Studio</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.78rem;color:{SUBTEXT};margin-bottom:16px;'>Powered by Groq</p>", unsafe_allow_html=True)

    # ── Tool navigation with active highlight ──
    st.markdown(f"<p style='font-size:0.72rem;color:{SUBTEXT};text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;'>Tools</p>", unsafe_allow_html=True)

    for t in ["💬 Chat", "📝 Summarize", "✍️ Generate"]:
        is_active = st.session_state.tool == t
        container = st.container()
        with container:
            if is_active:
                st.markdown('<div class="active-tool">', unsafe_allow_html=True)
            if st.button(t, key=f"nav_{t}", use_container_width=True):
                st.session_state.tool = t
                st.rerun()
            if is_active:
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Model selector ──
    st.markdown(f"<p style='font-size:0.72rem;color:{SUBTEXT};text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;'>Model</p>", unsafe_allow_html=True)
    selected_model_name = st.selectbox("model", list(MODELS.keys()), label_visibility="collapsed")
    selected_model = MODELS[selected_model_name]

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Theme toggle ──
    theme_label = "☀️  Light Mode" if dark else "🌙  Dark Mode"
    if st.button(theme_label, key="theme_btn", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    # ── Clear chat (only in Chat tab) ──
    if st.session_state.tool == "💬 Chat":
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🗑  Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.chat_input_val = ""
            st.rerun()

# ── Main content ──────────────────────────────────────────────────────────────
tool = st.session_state.tool

# ════════════════════════════════════════════════════════
# 💬  CHAT
# ════════════════════════════════════════════════════════
if tool == "💬 Chat":
    st.markdown("<div class='section-title'>Chat</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-sub'>Multi-turn conversation — your history is preserved.</div>", unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.chat_history:
        cls = "bubble-user" if msg["role"] == "user" else "bubble-ai"
        st.markdown(f"<div class='{cls}'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input — uses session state value so we can clear it after send
    user_input = st.text_area(
        "message",
        value=st.session_state.chat_input_val,
        placeholder="Type your message and click Send…",
        height=110,
        label_visibility="collapsed",
        key="chat_textarea"
    )

    col_send, col_space = st.columns([1, 5])
    with col_send:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        send = st.button("Send →", key="chat_send")
        st.markdown('</div>', unsafe_allow_html=True)

    if send:
        if user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_input_val = ""   # ← clears the text area
            with st.spinner("Thinking…"):
                try:
                    reply = chat(st.session_state.chat_history, model=selected_model)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")
            st.rerun()
        else:
            st.warning("Please enter a message.")

# ════════════════════════════════════════════════════════
# 📝  SUMMARIZE
# ════════════════════════════════════════════════════════
elif tool == "📝 Summarize":
    st.markdown("<div class='section-title'>Summarize</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-sub'>Paste any text and get a clean, concise summary.</div>", unsafe_allow_html=True)

    text_input = st.text_area(
        "text",
        placeholder="Paste an article, notes, or any text here…",
        height=220,
        label_visibility="collapsed",
        key="sum_input"
    )

    col_btn, _ = st.columns([1, 5])
    with col_btn:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        do_sum = st.button("Summarize →", key="sum_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if do_sum:
        if text_input.strip():
            with st.spinner("Summarizing…"):
                try:
                    st.session_state.sum_result = summarize(text_input, model=selected_model)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please paste some text first.")

    if st.session_state.sum_result:
        st.markdown(f"<div class='output-card'>{st.session_state.sum_result}</div>", unsafe_allow_html=True)
        st.text_area("📋 Copy output", value=st.session_state.sum_result, height=140, key="sum_copy")

# ════════════════════════════════════════════════════════
# ✍️  GENERATE
# ════════════════════════════════════════════════════════
elif tool == "✍️ Generate":
    st.markdown("<div class='section-title'>Generate</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-sub'>Create blogs, emails, code, social posts & more.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        content_type = st.selectbox("Type", ["Blog Post", "Email", "Code", "Social Media Post", "Essay"])
    with col2:
        topic = st.text_input(
            "topic",
            placeholder="e.g. Benefits of AI in healthcare",
            label_visibility="collapsed",
            key="gen_topic"
        )

    col_btn2, _ = st.columns([1, 5])
    with col_btn2:
        st.markdown('<div class="action-btn">', unsafe_allow_html=True)
        do_gen = st.button("Generate →", key="gen_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if do_gen:
        if topic.strip():
            with st.spinner("Generating…"):
                try:
                    st.session_state.gen_result = generate_content(content_type, topic, model=selected_model)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a topic.")

    if st.session_state.gen_result:
        st.markdown(f"<div class='output-card'>{st.session_state.gen_result}</div>", unsafe_allow_html=True)
        st.text_area("📋 Copy output", value=st.session_state.gen_result, height=140, key="gen_copy")