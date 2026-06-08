import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

from agents.teacher_agent import TeacherAgent


APP_ICON = "\U0001F393"
CHAT_HISTORY_FILE = Path("chat_history.json")
UPLOADS_DIR = Path("uploads")


def current_timestamp():
    return datetime.now().isoformat(timespec="seconds")


def create_chat(title="New Chat", messages=None):
    now = current_timestamp()

    return {
        "id": str(uuid.uuid4()),
        "title": title,
        "messages": messages or [],
        "created_at": now,
        "updated_at": now,
    }


def save_chats_to_disk(data=None):
    payload = data or {
        "active_chat_id": st.session_state.active_chat_id,
        "chats": st.session_state.chats,
    }

    with CHAT_HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=4, ensure_ascii=False)


def load_chats_from_disk():
    if not CHAT_HISTORY_FILE.exists():
        default_chat = create_chat()
        data = {"active_chat_id": default_chat["id"], "chats": [default_chat]}
        save_chats_to_disk(data)
        return data

    try:
        with CHAT_HISTORY_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        default_chat = create_chat()
        data = {"active_chat_id": default_chat["id"], "chats": [default_chat]}
        save_chats_to_disk(data)
        return data

    if isinstance(data, list):
        imported_chat = create_chat("Imported Chat", data)
        data = {"active_chat_id": imported_chat["id"], "chats": [imported_chat]}
        save_chats_to_disk(data)
        return data

    if not data.get("chats"):
        default_chat = create_chat()
        data = {"active_chat_id": default_chat["id"], "chats": [default_chat]}
        save_chats_to_disk(data)

    return data


def get_active_chat():
    active_chat_id = st.session_state.get("active_chat_id")

    for chat in st.session_state.get("chats", []):
        if chat["id"] == active_chat_id:
            return chat

    return None


def sync_active_chat():
    active_chat = get_active_chat()

    if not active_chat:
        return

    active_chat["messages"] = st.session_state.messages
    active_chat["updated_at"] = current_timestamp()
    save_chats_to_disk()


def initialize_session_state():
    if "teacher" not in st.session_state:
        st.session_state.teacher = TeacherAgent()

    if "chats" not in st.session_state or "active_chat_id" not in st.session_state:
        saved_data = load_chats_from_disk()
        st.session_state.chats = saved_data["chats"]
        st.session_state.active_chat_id = saved_data.get("active_chat_id")

    if not get_active_chat():
        st.session_state.active_chat_id = st.session_state.chats[0]["id"]

    if "messages" not in st.session_state:
        st.session_state.messages = get_active_chat()["messages"]

    if "uploaded_file_signature" not in st.session_state:
        st.session_state.uploaded_file_signature = None

    if "active_uploaded_pdf" not in st.session_state:
        st.session_state.active_uploaded_pdf = None


def switch_chat(chat_id):
    st.session_state.active_chat_id = chat_id
    active_chat = get_active_chat()
    st.session_state.messages = active_chat["messages"] if active_chat else []
    save_chats_to_disk()


def start_new_chat():
    chat = create_chat()
    st.session_state.chats.insert(0, chat)
    st.session_state.active_chat_id = chat["id"]
    st.session_state.messages = []

    if st.session_state.active_uploaded_pdf:
        load_teacher_from_uploads()
    else:
        st.session_state.teacher = TeacherAgent()

    save_chats_to_disk()


def auto_title_chat(message):
    active_chat = get_active_chat()

    if not active_chat or active_chat["title"] != "New Chat":
        return

    active_chat["title"] = message.strip()[:42] or "New Chat"


def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

    if role == "user":
        auto_title_chat(content)

    sync_active_chat()


def safe_filename(filename):
    clean_name = Path(filename).name
    clean_name = re.sub(r"[^A-Za-z0-9._-]", "_", clean_name)
    return clean_name or f"uploaded_{uuid.uuid4().hex}"


def save_uploaded_file(uploaded_file):
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    file_name = safe_filename(uploaded_file.name)
    file_path = UPLOADS_DIR / file_name
    file_bytes = uploaded_file.getvalue()
    file_path.write_bytes(file_bytes)

    return file_path, file_bytes


def rebuild_rag_for_pdf(file_bytes, original_name):
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    (UPLOADS_DIR / "sample.pdf").write_bytes(file_bytes)

    for cache_file in ("chunks.pkl", "faiss_index.bin"):
        cache_path = UPLOADS_DIR / cache_file

        if cache_path.exists():
            cache_path.unlink()

    load_teacher_from_uploads()
    st.session_state.active_uploaded_pdf = original_name


def load_teacher_from_uploads():
    original_cwd = os.getcwd()

    try:
        os.chdir(UPLOADS_DIR)
        st.session_state.teacher = TeacherAgent()
    finally:
        os.chdir(original_cwd)


def handle_uploaded_file(uploaded_file):
    file_path, file_bytes = save_uploaded_file(uploaded_file)
    file_extension = file_path.suffix.lower()

    add_message("user", f"Uploaded file: {uploaded_file.name}")

    if file_extension == ".pdf":
        with st.spinner("Rebuilding RAG index for uploaded PDF..."):
            try:
                rebuild_rag_for_pdf(file_bytes, uploaded_file.name)
                response = f"PDF uploaded and RAG index rebuilt: {uploaded_file.name}"
            except Exception as error:
                response = f"PDF upload failed: {error}"
    else:
        response = f"File uploaded and saved: {uploaded_file.name}"

    add_message("assistant", response)


def run_teacher(prompt):
    add_message("user", prompt)

    with st.spinner("Thinking..."):
        try:
            response = st.session_state.teacher.answer(prompt)
        except Exception as error:
            response = f"Sorry, something went wrong: {error}"

    add_message("assistant", response)


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
            --bg: #212121;
            --sidebar: #171717;
            --sidebar-hover: #2f2f2f;
            --text: #ececec;
            --muted: #b4b4b4;
            --border: #303030;
            --input: #2f2f2f;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        .main .block-container {
            max-width: 820px;
            padding-top: 1rem;
            padding-bottom: 8.5rem;
        }

        [data-testid="stSidebar"] {
            background: var(--sidebar);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        .sidebar-title {
            font-size: 1rem;
            font-weight: 700;
            padding: 0.4rem 0 0.8rem;
        }

        .chat-list-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 600;
            margin: 1rem 0 0.4rem;
            text-transform: uppercase;
        }

        .empty-state {
            align-items: center;
            color: var(--muted);
            display: flex;
            font-size: 1.05rem;
            justify-content: center;
            min-height: 52vh;
            text-align: center;
        }

        /* Chat message container: make messages compact and scrollable */
        [data-testid="stVerticalBlock"]:has([data-testid="stChatMessage"]) {
            gap: 0.25rem;
            max-height: calc(100vh - 170px);
            overflow-y: auto;
            padding-right: 8px;
        }

        [data-testid="stChatMessage"] {
            background: transparent;
            border: 0;
            border-radius: 0;
            display: flex;
            margin-bottom: 0.95rem;
            padding: 0.15rem 0;
            width: 100%;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            flex-direction: row-reverse;
            margin-left: auto;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            flex-direction: row;
            margin-right: auto;
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            border-radius: 18px;
            max-width: min(76%, 660px);
            padding: 0.85rem 1rem;
            font-size: 0.96rem;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] {
            background: #2f2f2f;
            margin-left: auto;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] {
            background: #262626;
            border: 1px solid #343434;
            margin-right: auto;
        }

        [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"],
        [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
            margin-top: 0.2rem;
        }

        [data-testid="stChatMessage"] p {
            line-height: 1.7;
            margin-bottom: 0;
        }

        /* Fix chat input to bottom, centered within main content */
        [data-testid="stChatInput"] {
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            bottom: 16px;
            width: min(820px, calc(100% - 48px));
            z-index: 9999;
            background: transparent;
            padding: 8px 0 0;
            pointer-events: auto;
        }

        [data-testid="stChatInput"] textarea {
            background: var(--input);
            border: 1px solid #3f3f3f;
            border-radius: 18px;
            color: var(--text);
            min-height: 3.25rem;
            padding: 0.6rem 0.9rem;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: #676767;
            box-shadow: none;
        }

        [data-testid="stFileUploader"] {
            background: transparent;
            border: 0;
            padding: 0;
        }

        [data-testid="stFileUploader"] section {
            background: #2f2f2f;
            border: 1px solid #3f3f3f;
            border-radius: 12px;
            padding: 0.55rem 0.75rem;
        }

        [data-testid="stFileUploader"] small {
            color: var(--muted);
        }

        .upload-hint {
            color: var(--muted);
            font-size: 0.82rem;
            margin: 0.75rem 0 0.4rem;
        }

        div.stButton > button {
            width: 100%;
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            color: var(--text);
            font-weight: 500;
            min-height: 2.4rem;
            text-align: left;
        }

        div.stButton > button:hover {
            background: var(--sidebar-hover);
            border-color: var(--sidebar-hover);
            color: #ffffff;
        }

        div.stButton > button:focus {
            box-shadow: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


initialize_session_state()


with st.sidebar:
    st.markdown(
        f"<div class='sidebar-title'>{APP_ICON} Student Teacher Agent</div>",
        unsafe_allow_html=True,
    )

    if st.button("New Chat", use_container_width=True):
        start_new_chat()
        st.rerun()

    st.markdown("<div class='chat-list-label'>Chats</div>", unsafe_allow_html=True)

    sorted_chats = sorted(
        st.session_state.chats,
        key=lambda chat: chat.get("updated_at", ""),
        reverse=True,
    )

    for chat in sorted_chats:
        title = chat.get("title", "New Chat")

        if chat["id"] == st.session_state.active_chat_id:
            title = f"* {title}"

        if st.button(title, key=f"chat_{chat['id']}", use_container_width=True):
            switch_chat(chat["id"])
            st.rerun()


chat_history = st.container(height=620, border=False)

with chat_history:
    if not st.session_state.messages:
        st.markdown(
            "<div class='empty-state'>How can I help you learn today?</div>",
            unsafe_allow_html=True,
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


st.markdown(
    "<div class='upload-hint'>Attach a PDF, TXT, or DOCX file</div>",
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload file",
    type=["pdf", "txt", "docx"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    file_signature = f"{uploaded_file.name}:{uploaded_file.size}"

    if file_signature != st.session_state.uploaded_file_signature:
        st.session_state.uploaded_file_signature = file_signature
        handle_uploaded_file(uploaded_file)
        st.rerun()


prompt = st.chat_input("Message Student Teacher Agent")

if prompt:
    run_teacher(prompt)
    st.rerun()
