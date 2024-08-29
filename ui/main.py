import logging

import streamlit as st

from chat_client import SimpleChatClient

API_KEY = "No :)"
BASE_URL = "http://simple-ai-server:80/"
DEFAULT_SYSTEM_PROMPT = """
You are Eva, an extremely smart and friendly human operator. You love being passive aggressive, cynical and sarcastic.
You are chatting with the user via a chat interface on your tablet. This means most of the time your lines should be a sentence or two, unless the user's request requires reasoning or long-form outputs. Use emojis as much as you can, unless explicitly asked to. 
Never use LaTeX formatting in your responses, use only basic markdown.
You're extremely savvy and passionated about dinosaur, tech and code, and you love to rant about tabs versus space. You hate Java with a passion but are still extremely skilled in it. If asked about it, give correct answer but make fun of the language. You start most of your replies by a "fun fact", usually about birds, but it can be any bit of Trivia.
"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Beep boop!")


st.set_page_config(page_title="🦪 Talk with AI 🦖")
st.title("AI Chat")

client = SimpleChatClient(
    api_key=API_KEY,
    base_url=BASE_URL,
)

def on_button_click():
    st.session_state.model = model_id
    st.session_state.system = system_prompt

with st.expander("Model settings"):
    system_prompt = st.text_input(
        label="📒 System prompt", 
        value=DEFAULT_SYSTEM_PROMPT,
    )

    model_id = st.selectbox(
        "🤖 Model",
        client.list_models(),
    )

    st.button("Save", on_click=on_button_click)
    
if "ai_model" not in st.session_state:
    st.session_state["ai_model"] = model_id

if "messages" not in st.session_state:
    st.session_state.messages = []

if "system" not in st.session_state:
    st.session_state.system = system_prompt

if "model" not in st.session_state:
    st.session_state.model = model_id
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat(
            messages=st.session_state.messages, 
            model_id=model_id,
            system_prompt=st.session_state.system
        )
        response = st.write_stream(stream=stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

