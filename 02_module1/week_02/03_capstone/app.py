import warnings

import streamlit as st
from llm_providers import run_llm

warnings.filterwarnings("ignore")


st.set_page_config(page_title="My First AI Chat Assistant", page_icon=":robot_face:")
st.title("My First AI Chat Assistant")

# initialize conversation memory

if "history" not in st.session_state:
    st.session_state["history"] = [
        {"role": "assistant", "content": "Hi! How can i help you today?"}
    ]

# Display chat history

for msg in st.session_state["history"]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# user input

if prompt := st.chat_input("Type your message..."):
    # add user message
    st.session_state["history"].append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    reply = run_llm(st.session_state["history"])

    st.session_state["history"].append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

if st.button("Reset History:"):
    st.session_state["history"] = [
        {"role": "assistant", "content": "Hi! How can i help you today?"}
    ]
    st.rerun()
