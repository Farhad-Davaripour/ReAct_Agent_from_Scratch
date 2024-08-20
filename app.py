import os
import streamlit as st
import importlib
import src.tools as tools
import yaml
import json
import textwrap
importlib.reload(tools)
from src.tools import query, retrieve_tasks, retrieve_resources
import re

# Create two columns
col1, col2 = st.columns([3, 1.2])

with col1:
    # Setting the title and configuring the layout of the Streamlit page
    st.title("ReAct Agentic Workflow")


with col2:
    # Ensure the environment variable for the figure path is correctly set
    logo_file_path = "artifacts/arcurve_logo.jpeg"
    print(logo_file_path)
    if logo_file_path and os.path.exists(logo_file_path):
        st.image(logo_file_path, width=200)
    else:
        st.error("Figure path is not set correctly or the file does not exist.")


with st.expander("Problem Statement:"):
    st.markdown("""
    This example simulates a project management scenario where we need to allocate resources to various tasks.
    The ReAct Agent will help us assign resources based on task priorities and resource availability.
    
    Below are the tasks and available resources for this simulation:
    """)

    # Display tasks
    st.markdown("**Active Tasks:**")
    st.markdown("These tasks represent different project components with varying priorities and estimated effort in hours.")
    tasks = retrieve_tasks()
    st.table(tasks)

    # Display resources
    st.markdown("**Available Resources:**")
    st.markdown("These resources represent team members with different skills and available hours for the project.")
    resources = retrieve_resources()
    st.table(resources)

def format_system_prompt(prompt):
    # Split the prompt into sections
    sections = re.split(r'\n\n+', prompt)
    formatted_sections = []
    
    for section in sections:
        if ':' in section:
            # For sections with a title
            title, content = section.split(':', 1)
            content = content.strip()
            if '\n' in content:
                formatted_sections.append(f"{title}:\n{textwrap.indent(content, '  ')}")
            else:
                formatted_sections.append(f"{title}: {content}")
        elif section.startswith('Example session'):
            # For the example session
            formatted_sections.append("Example session:")
            example = section[16:].strip()
            formatted_sections.append(textwrap.indent(example, '  '))
        else:
            # For other sections
            formatted_sections.append(section)
    
    return '\n\n'.join(formatted_sections)

known_actions = {
    "retrieve_tasks": retrieve_tasks,
    "retrieve_resources": retrieve_resources,
}

question_st = "Allocate resources to high-priority tasks." #"Allocate resources to high-priority tasks, summarize the allocation, and estimate the total budget."
question = st.text_input("Question:", value=question_st)


max_turns = 5

if st.button("Run"):
    with st.spinner("Processing your query..."):
        reasoning, result = query(question, max_turns, known_actions, "gpt-4o")
        
        # Reasoning in a collapsible box without nested expanders
        with st.expander("Show Reasoning"):
            st.markdown("### Reasoning:")
            for i, message in enumerate(reasoning):
                st.markdown(f"**{i+1}. {message['role'].capitalize()} Prompt:**")
                if message['role'] == 'system':
                    st.code(format_system_prompt(message['content']), language='yaml')
                else:
                    st.json(message)

        # Use regex to extract the part after "Answer:"
        extracted_answer = re.search(r'Answer:\s*(.*)', result, re.DOTALL)
        if extracted_answer:
            st.markdown(f"### Final Answer:\n{extracted_answer.group(1)}")
        else:
            st.markdown(f"### Final Result:\n{result}")