import streamlit as st
from src.model import rag_chain

st.set_page_config(page_title="MediBot", page_icon="💊")
st.title("💊 MediBot")

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for msg in st.session_state["message_history"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("What is you query...")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        stream_box = st.empty()
        full_response = ""

        context_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state["message_history"]
        ]

        for chunk in rag_chain.stream(
            {"input": user_input, "history": context_messages}
        ):
            if "answer" in chunk:
                full_response += chunk["answer"]
                stream_box.write(full_response)

    st.session_state["message_history"].append(
        {"role": "assistant", "content": full_response}
    )
