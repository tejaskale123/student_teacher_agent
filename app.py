import streamlit as st
from agents.teacher_agent import TeacherAgent

st.title("Student Teacher Agent")

if "teacher" not in st.session_state:
    st.session_state.teacher = TeacherAgent()

question = st.text_input("Ask a question")

if st.button("Send"):

    answer = st.session_state.teacher.answer(
        question
    )

    st.write("### Answer")
    st.write(answer)