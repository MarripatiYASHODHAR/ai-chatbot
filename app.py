import streamlit as st
import os

import numpy as np
import requests

from sentence_transformers import SentenceTransformer
from groq import Groq

# =========================
# Imports & Config
# =========================
import streamlit as st
from utils.rag_utils import load_docs, create_index, search
from utils.web_search import search_web
from models.llm import get_llm_response

# =========================
# Streamlit UI Setup
# =========================
st.set_page_config(page_title="Enterprise Knowledge Assistant", layout="centered")
st.title("💼 Enterprise Knowledge Assistant")
st.markdown("""
Ask questions about company documents or general topics. Powered by RAG, web search fallback, and Groq LLM.
""")

# =========================
# Sidebar Branding & Links
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
    st.markdown("**Enterprise Knowledge Assistant**")
    st.markdown("---")
    st.markdown("Empowering employees with instant access to company knowledge and documents.")
    st.markdown("---")


# =========================
# Response Mode Selection
# =========================
mode = st.radio("Response Mode:", ["Concise", "Detailed"])

# =========================
# Load Documents & Index (RAG)
# =========================
@st.cache_resource(show_spinner=False)
def setup_rag():
    load_docs()
    return create_index()

if "index" not in st.session_state:
    st.session_state.index = setup_rag()

# =========================
# User Input
# =========================

st.markdown("---")
st.markdown("### Ask the Assistant")
query = st.text_input("Enter your question:", placeholder="e.g. How do I apply for leave?")
response = ""
st.markdown("---")


# =========================
# Main Chatbot Logic
# =========================
if st.button("Ask"):
    try:
        index = st.session_state.index
        doc_context = search(query, index)
        # If context is relevant, use it; else fallback to web search
        if doc_context and len(doc_context.strip()) > 20:
            prompt = f"User Query: {query}\nMode: {mode}. Respond concisely or in detail as requested. Avoid hallucinations."
            response = get_llm_response(prompt, context=doc_context)
        else:
            web_result = search_web(query)
            prompt = f"User Query: {query}\nMode: {mode}. Respond concisely or in detail as requested. Avoid hallucinations."
            response = get_llm_response(prompt, context=web_result)
    except Exception as e:
        response = f"Error: {e}"

# =========================
# Display Response
# =========================
if response:
    st.markdown("### 🤖 Response")
    st.info(response)



