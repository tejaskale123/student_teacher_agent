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
            padding: 0;
            pointer-events: auto;
        }

        [data-testid="stChatInput"] textarea {
            background: var(--input);
            border: 1px solid #3f3f3f;
            border-radius: 24px;
            color: var(--text);
            min-height: 3.2rem;
            padding: 0.75rem 1rem 0.75rem 3.5rem;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: #676767;
            box-shadow: none;
        }

        button[title="Upload a file"] {
            position: fixed;
            left: calc(50% - 402px);
            bottom: 20px;
            width: 3rem;
            height: 3rem;
            border-radius: 16px;
            background: #2f2f2f;
            border: 1px solid #444;
            color: var(--text);
            font-size: 22px;
            padding: 0;
            z-index: 10010;
        }

        button[title="Upload a file"]:hover {
            background: #383838;
        }

        .attachment-popup {
            position: fixed;
            left: 50%;
            transform: translateX(-50%);
            bottom: 72px;
            width: min(820px, calc(100% - 48px));
            z-index: 10009;
            background: #1f1f1f;
            border: 1px solid #363636;
            border-radius: 16px;
            padding: 0.8rem 0.95rem;
            margin-bottom: 0;
        }

        .upload-preview {
            background: #202020;
            border: 1px solid #333333;
            border-radius: 14px;
            color: var(--text);
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem 1rem;
            margin-bottom: 0.65rem;
            width: fit-content;
        }

        .upload-preview span {
            font-size: 0.95rem;
        }

        .upload-ready {
            color: #8df57f;
            font-weight: 600;
        }

        .attachment-popup {
            background: #1f1f1f;
            border: 1px solid #363636;
            border-radius: 16px;
            padding: 0.9rem 1rem;
            margin-bottom: 0.6rem;
        }

        .attachment-popup div {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
        }

        .attachment-popup button {
            min-width: 118px;
            border-radius: 14px;
            border: 1px solid #3f3f3f;
            background: #232323;
            color: var(--text);
            padding: 0.55rem 0.75rem;
            cursor: pointer;
        }

        .attachment-popup button:hover {
            background: #2d2d2d;
        }

        .attachment-success {
            color: #8df57f;
            font-size: 0.92rem;
            margin-top: 0.3rem;
        }

        .attach-row {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            width: 100%;
            margin-bottom: 0.2rem;
        }

        .attach-button button {
            background: #2f2f2f;
            border: 1px solid #444;
            border-radius: 14px;
            color: var(--text);
            min-height: 3rem;
            width: 3rem;
            font-size: 20px;
            padding: 0;
        }

        .attach-button button:hover {
            background: #383838;
        }

        .attachment-popup {
            background: #1f1f1f;
            border: 1px solid #363636;
            border-radius: 16px;
            padding: 0.8rem 0.95rem;
            margin-bottom: 0.55rem;
        }

        .attachment-popup div {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
        }

        .attachment-popup button {
            min-width: 120px;
            border-radius: 14px;
            border: 1px solid #3f3f3f;
            background: #232323;
            color: var(--text);
            padding: 0.55rem 0.75rem;
            cursor: pointer;
        }

        .attachment-popup button:hover {
            background: #2d2d2d;
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

        /* Sidebar specific tweaks */
        [data-testid="stSidebar"] .chat-list .stButton > button {
            border-radius: 8px;
            padding-left: 0.6rem;
            padding-right: 0.6rem;
            text-align: left;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        [data-testid="stSidebar"] .chat-list .stButton > button:hover {
            background: #272727;
            transform: translateY(-1px);
            cursor: pointer;
        }

        [data-testid="stSidebar"] .chat-list .stButton > button:active {
            transform: translateY(0);
        }

        .chat-list-label {
            margin-top: 0.6rem;
        }

        /* Attachment button beside chat input */
        .attach-link {
            position: fixed;
            bottom: 22px;
            left: calc(50% - 420px);
            width: 40px;
            height: 40px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: #2f2f2f;
            border-radius: 10px;
            border: 1px solid #3f3f3f;
            color: var(--text);
            text-decoration: none;
            z-index: 10001;
            font-size: 18px;
        }

        .attachment-panel {
            position: fixed;
            bottom: 72px;
            left: calc(50% - 220px);
            width: 440px;
            z-index: 10001;
            background: transparent;
        }

        .attachment-panel .stFileUploader section {
            display: flex;
            gap: 8px;
            align-items: center;
            padding: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


initialize_session_state()


with st.sidebar:
    # Top title
    st.markdown(
        f"<div class='sidebar-title'>{APP_ICON} Student Teacher Agent</div>",
        unsafe_allow_html=True,
    )

    # Single New Chat button
    if st.button("+  New chat", key="new_chat_sidebar", use_container_width=True):
        start_new_chat()
        st.rerun()

    st.markdown("<div class='chat-list-label'>Chats</div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='chat-list' style='max-height:60vh; overflow:auto; padding-right:6px;'>",
        unsafe_allow_html=True,
    )

    sorted_chats = sorted(
        st.session_state.chats,
        key=lambda chat: chat.get("updated_at", ""),
        reverse=True,
    )

    def truncate(text, n=30):
        return text if len(text) <= n else text[: n - 3].rstrip() + "..."

    for chat in sorted_chats:
        chat_id = chat["id"]
        title = chat.get("title", "New Chat")
        is_active = chat_id == st.session_state.active_chat_id

        cols = st.columns([0.08, 0.72, 0.2])

        with cols[0]:
            st.markdown("💬")

        display_title = truncate(title, 28)
        button_label = f"{display_title}"
        if is_active:
            button_label = f"● {display_title}"

        with cols[1]:
            if st.button(button_label, key=f"chat_select_{chat_id}", help=title):
                switch_chat(chat_id)
                st.rerun()

        with cols[2]:
            if st.button("⋮", key=f"menu_{chat_id}"):
                if st.session_state.get("_menu_for") == chat_id:
                    st.session_state._menu_for = None
                else:
                    st.session_state._menu_for = chat_id

        if st.session_state.get("_menu_for") == chat_id:
            action_cols = st.columns([0.5, 0.5])
            with action_cols[0]:
                if st.button("Rename", key=f"rename_action_{chat_id}"):
                    st.session_state._rename_for = chat_id
                    st.session_state._delete_for = None

            with action_cols[1]:
                if st.button("Delete", key=f"delete_action_{chat_id}"):
                    st.session_state._delete_for = chat_id
                    st.session_state._rename_for = None

            if st.session_state.get("_rename_for") == chat_id:
                new_name = st.text_input(
                    "New name",
                    key=f"rename_input_{chat_id}",
                    value=title,
                    label_visibility="collapsed",
                )
                if st.button("Save", key=f"save_rename_{chat_id}"):
                    if new_name:
                        for c in st.session_state.chats:
                            if c["id"] == chat_id:
                                c["title"] = new_name
                                break
                        save_chats_to_disk()
                        st.session_state._menu_for = None
                        st.session_state._rename_for = None
                        st.rerun()
                if st.button("Cancel", key=f"cancel_rename_{chat_id}"):
                    st.session_state._rename_for = None
                    st.session_state._menu_for = None
                    st.rerun()

            if st.session_state.get("_delete_for") == chat_id:
                confirm_delete = st.checkbox("Confirm delete", key=f"delete_confirm_{chat_id}")
                if confirm_delete and st.button("Delete permanently", key=f"confirm_delete_{chat_id}"):
                    st.session_state.chats = [c for c in st.session_state.chats if c["id"] != chat_id]
                    if st.session_state.get("active_chat_id") == chat_id:
                        st.session_state.active_chat_id = st.session_state.chats[0]["id"] if st.session_state.chats else None
                        st.session_state.messages = get_active_chat()["messages"] if st.session_state.active_chat_id else []
                    save_chats_to_disk()
                    st.session_state._menu_for = None
                    st.session_state._delete_for = None
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


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


if "attachment_menu_open" not in st.session_state:
    st.session_state.attachment_menu_open = False

if "attachment_type" not in st.session_state:
    st.session_state.attachment_type = None

if "uploaded_preview" not in st.session_state:
    st.session_state.uploaded_preview = None

if "upload_status" not in st.session_state:
    st.session_state.upload_status = None

if st.session_state.uploaded_preview:
    st.markdown(
        f"<div class='upload-preview'>📄 {st.session_state.uploaded_preview} <span class='upload-ready'>{st.session_state.upload_status or 'Ready'}</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='attachment-success'>File uploaded successfully.</div>",
        unsafe_allow_html=True,
    )

if st.session_state.attachment_menu_open:
    st.markdown("<div class='attachment-popup'>", unsafe_allow_html=True)
    option_cols = st.columns([1, 1, 1, 1])

    with option_cols[0]:
        if st.button("📄 Upload PDF", key="upload_pdf"):
            st.session_state.attachment_type = "pdf"
    with option_cols[1]:
        if st.button("🖼 Upload Image", key="upload_image"):
            st.session_state.attachment_type = "image"
    with option_cols[2]:
        if st.button("📄 Upload DOCX", key="upload_docx"):
            st.session_state.attachment_type = "docx"
    with option_cols[3]:
        if st.button("📄 Upload TXT", key="upload_txt"):
            st.session_state.attachment_type = "txt"

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.attachment_type:
        if st.session_state.attachment_type == "pdf":
            allowed_types = ["pdf"]
            label = "Choose a PDF file"
        elif st.session_state.attachment_type == "image":
            allowed_types = ["png", "jpg", "jpeg"]
            label = "Choose an image file"
        elif st.session_state.attachment_type == "docx":
            allowed_types = ["docx"]
            label = "Choose a DOCX file"
        else:
            allowed_types = ["txt"]
            label = "Choose a TXT file"

        attachment = st.file_uploader(
            label,
            type=allowed_types,
            key="attachment_uploader",
            label_visibility="visible",
        )

        if attachment is not None:
            file_signature = f"{attachment.name}:{attachment.size}"
            if file_signature != st.session_state.uploaded_file_signature:
                st.session_state.uploaded_file_signature = file_signature
                handle_uploaded_file(attachment)
                st.session_state.uploaded_preview = attachment.name
                st.session_state.upload_status = "Ready"
                st.session_state.attachment_menu_open = False
                st.session_state.attachment_type = None
                st.rerun()

if st.button("+", key="attach_btn", help="Upload a file"):
    st.session_state.attachment_menu_open = not st.session_state.attachment_menu_open
    st.session_state.attachment_type = None

prompt = st.chat_input("Message Student Teacher Agent")

if prompt:
    run_teacher(prompt)
    st.rerun()
