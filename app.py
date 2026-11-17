"""Password-protected web chat for Groq, built with Streamlit.

Run locally:   streamlit run app.py
Deploy:        Streamlit Community Cloud (see README).
Secrets:       GROQ_API_KEY, APP_PASSWORD  (st.secrets or environment / .env)
"""
import hmac
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

BASE_URL = "https://api.groq.com/openai/v1"
MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]


def secret(name: str, default: str = "") -> str:
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:  # no secrets.toml present
        pass
    return os.getenv(name, default)


st.set_page_config(page_title="Groq Chat", page_icon="💬")

# ---- Password gate -------------------------------------------------------
password = secret("APP_PASSWORD")
if not password:
    st.error("APP_PASSWORD is not configured. Add it to the app's secrets.")
    st.stop()

if not st.session_state.get("authed"):
    st.title("💬 Groq Chat")
    with st.form("login"):
        attempt = st.text_input("Password", type="password")
        if st.form_submit_button("Enter"):
            if hmac.compare_digest(attempt.encode(), password.encode()):
                st.session_state.authed = True
                st.rerun()
            else:
                st.error("Wrong password.")
    st.stop()

# ---- Chat ----------------------------------------------------------------
api_key = secret("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY is not configured. Add it to the app's secrets.")
    st.stop()

client = OpenAI(base_url=BASE_URL, api_key=api_key)
default_model = secret("GROQ_MODEL", MODELS[0])

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model", MODELS, index=MODELS.index(default_model) if default_model in MODELS else 0
    )
    system_prompt = st.text_area("System prompt", "You are a helpful assistant.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

st.title("💬 Groq Chat")
st.session_state.setdefault("messages", [])

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask anything…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}]
                + st.session_state.messages,
                stream=True,
            )
            reply = st.write_stream(
                c.choices[0].delta.content or ""
                for c in stream
                if c.choices
            )
        except Exception as e:  # rate limit, bad key, etc.
            reply = ""
            st.error(f"Request failed: {e}")
    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
