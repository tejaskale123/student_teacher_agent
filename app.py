import os

import streamlit as st

from agents.teacher_agent import TeacherAgent


APP_ICON = "\U0001F393"

QUICK_ACTIONS = {
    "Summarize PDF": "Summarize the PDF in simple bullet points.",
    "Python Functions": "What are Python functions? Explain with a simple example.",
    "AI News": "Search the latest AI news and summarize the most important updates.",
    "Calculator": "Calculate 25 * 4 + 18 / 3.",
}


st.set_page_config(
    page_title="Student Teacher Agent",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        :root {
            --bg: #0b1020;
            --panel: #111827;
            --panel-soft: #151c2f;
            --card: #121a2b;
            --border: #26324a;
            --text: #f8fafc;
            --muted: #9ca3af;
            --accent: #7c8cff;
            --accent-soft: rgba(124, 140, 255, 0.14);
            --success: #22c55e;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(124, 140, 255, 0.16), transparent 32rem),
                linear-gradient(180deg, #0b1020 0%, #0b0f19 100%);
            color: var(--text);
        }

        .main .block-container {
            max-width: 1020px;
            padding-top: 1.8rem;
            padding-bottom: 7rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #111827 0%, #0f172a 100%);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        .hero {
            border: 1px solid var(--border);
            background: linear-gradient(135deg, rgba(124, 140, 255, 0.18), rgba(18, 26, 43, 0.94));
            border-radius: 8px;
            padding: 1.35rem 1.45rem;
            margin-bottom: 1.2rem;
        }

        .hero-kicker {
            color: #c4b5fd;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 0.45rem;
            text-transform: uppercase;
        }

        .hero-title {
            color: var(--text);
            font-size: 2rem;
            font-weight: 780;
            letter-spacing: 0;
            line-height: 1.18;
            margin-bottom: 0.35rem;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 0.98rem;
            line-height: 1.55;
            max-width: 780px;
        }

        .sidebar-card {
            background: rgba(18, 26, 43, 0.88);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.95rem;
            margin-bottom: 0.8rem;
        }

        .sidebar-title {
            font-size: 0.96rem;
            font-weight: 750;
            margin-bottom: 0.45rem;
        }

        .sidebar-muted {
            color: var(--muted);
            font-size: 0.86rem;
            line-height: 1.5;
        }

        .status-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            padding: 0.55rem 0;
            border-bottom: 1px solid rgba(38, 50, 74, 0.7);
        }

        .status-row:last-child {
            border-bottom: 0;
            padding-bottom: 0;
        }

        .status-label {
            color: #dbeafe;
            font-size: 0.88rem;
            font-weight: 600;
        }

        .status-pill {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.45);
            border-radius: 999px;
            color: #86efac;
            font-size: 0.74rem;
            font-weight: 700;
            padding: 0.16rem 0.5rem;
            white-space: nowrap;
        }

        .status-pill.off {
            background: rgba(148, 163, 184, 0.12);
            border-color: rgba(148, 163, 184, 0.35);
            color: #cbd5e1;
        }

        [data-testid="stChatMessage"] {
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 0.85rem;
            padding: 0.78rem 1rem;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: rgba(31, 41, 55, 0.88);
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background: rgba(17, 24, 39, 0.9);
        }

        [data-testid="stChatMessage"] p {
            line-height: 1.65;
        }

        [data-testid="stChatInput"] textarea {
            background: #111827;
            border: 1px solid #334155;
            border-radius: 8px;
            color: var(--text);
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }

        div.stButton > button {
            width: 100%;
            border-radius: 8px;
            border: 1px solid #334155;
            background: #172033;
            color: var(--text);
            font-weight: 650;
            min-height: 2.45rem;
        }

        div.stButton > button:hover {
            border-color: var(--accent);
            background: #202a44;
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state():
    if "teacher" not in st.session_state:
        st.session_state.teacher = TeacherAgent()

    if "messages" not in st.session_state:
        st.session_state.messages = []


def clear_chat():
    st.session_state.messages = []
    st.session_state.teacher = TeacherAgent()


def status_pill(is_ready):
    if is_ready:
        return "<span class='status-pill'>Ready</span>"
    return "<span class='status-pill off'>Missing</span>"


def render_status_panel():
    pdf_ready = os.path.exists("sample.pdf")
    search_ready = hasattr(st.session_state.teacher, "search_tool")
    calculator_ready = hasattr(st.session_state.teacher, "calculator")

    st.markdown(
        f"""
        <div class="sidebar-card">
            <div class="sidebar-title">System Status</div>
            <div class="status-row">
                <span class="status-label">PDF Loaded</span>
                {status_pill(pdf_ready)}
            </div>
            <div class="status-row">
                <span class="status-label">Search Tool</span>
                {status_pill(search_ready)}
            </div>
            <div class="status-row">
                <span class="status-label">Calculator Tool</span>
                {status_pill(calculator_ready)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_message(role, content):
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


def run_teacher(prompt):
    add_message("user", prompt)

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.teacher.answer(prompt)
            except Exception as error:
                response = f"Sorry, something went wrong: {error}"

        st.write(response)

    add_message("assistant", response)


initialize_session_state()

quick_prompt = None

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Student Teacher Agent</div>
            <div class="sidebar-muted">Professional AI tutor workspace with chat, PDF RAG, search, calculator, and memory.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_status_panel()

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Quick Actions</div>
            <div class="sidebar-muted">Start with a common prompt.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for label, prompt_text in QUICK_ACTIONS.items():
        if st.button(label, use_container_width=True):
            quick_prompt = prompt_text

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    st.caption(f"Messages: {len(st.session_state.messages)}")


st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">AI Learning Workspace</div>
        <div class="hero-title">{APP_ICON} Student Teacher Agent</div>
        <div class="hero-subtitle">
            Ask questions, solve calculations, search live topics, or chat with your PDF content through your existing TeacherAgent backend.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write(
            "Hello! Ask me a study question, request a PDF summary, search a topic, or try a calculation."
        )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


typed_prompt = st.chat_input("Ask your teacher agent...")
prompt_to_process = quick_prompt or typed_prompt

if prompt_to_process:
    run_teacher(prompt_to_process)
