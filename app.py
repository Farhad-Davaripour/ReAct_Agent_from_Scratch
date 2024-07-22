import streamlit as st
import importlib
import src.tools as tools
import json
importlib.reload(tools)
from src.tools import calculate, query, retrieve_tasks, retrieve_resources, allocate_resources, estimate_budget

st.title("ReAct Agentic Workflow")

model_type = st.sidebar.selectbox("Model type:", ["gpt-4o", "gpt-3.5-turbo"])

known_actions = {
    "calculate": calculate,
    "retrieve_tasks": retrieve_tasks,
    "retrieve_resources": retrieve_resources,
    "allocate_resources": allocate_resources,
    "estimate_budget": lambda hours: estimate_budget(int(hours), hourly_rate=50)
}

question = st.text_input("Question", "Allocate resources to high-priority tasks, summarize the allocation, and estimate the total budget.")

max_turns = 5

if st.button("Run"):
    result = query(question, max_turns, known_actions, model_type)
    
    st.markdown("### Conversation:")
    for i, message in enumerate(result):
        with st.expander(f"{i+1.0}. {message['role'].capitalize()} Prompt"):
            st.json(message)