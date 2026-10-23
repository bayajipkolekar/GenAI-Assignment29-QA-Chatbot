
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from main import get_answer

st.set_page_config(
    page_title="Assignment 29 - Q&A Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Q&A Chatbot")
st.caption("Choose OpenAI or Ollama and ask your questions.")

model_type = st.sidebar.selectbox(
    "Choose AI Model",
    ["ollama", "openai"],
    format_func=lambda model: "Ollama (Local)" if model == "ollama" else "OpenAI (Cloud)"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = model_type

if st.session_state.selected_model != model_type:
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.selected_model = model_type

with st.sidebar:
    st.write("### Controls")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(
                question=question,
                model_type=model_type,
                chat_history=st.session_state.chat_history
            )
            st.markdown(answer)

    if not answer.startswith("Error:"):
        st.session_state.chat_history.append(
            HumanMessage(content=question)
        )
        st.session_state.chat_history.append(
            AIMessage(content=answer)
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
