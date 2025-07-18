import streamlit as st
import os
import tempfile
import gc
import base64
import time

from crewai import Agent, Crew, Process, Task, LLM
from src.tools.custom_tool import DocumentSearchTool
from crewai_tools import SerperDevTool 

@st.cache_resource
def load_llm():
    llm = LLM(model="gemini/gemini-2.0-flash")
    return llm

# ===========================
#   Define Agents & Tasks
# ===========================
def create_agents_and_tasks(pdf_tool):
    """Creates a Crew with the given PDF tool (if any) and a web search tool."""
    web_search_tool = SerperDevTool()

    retriever_agent = Agent(
        role="Retrieve relevant information to answer the user query: {query}",
        goal=(
            "Retrieve the most relevant information along with the metadata like source, page number, url from the available sources "
            "for the user query: {query}. Always try to use the PDF search tool first. "
            "If you are not able to retrieve the information from the PDF search tool, "
            "then try to use the web search tool."
        ),
        backstory=(
            "You're a meticulous analyst with a keen eye for detail. "
            "You're known for your ability to understand user queries: {query} "
            "and retrieve knowledge from the most suitable knowledge base."
        ),
        verbose=True,
        tools=[t for t in [pdf_tool, web_search_tool] if t],
        llm=load_llm()
    )

    response_synthesizer_agent = Agent(
        role="Response synthesizer agent for the user query: {query}",
        goal=(
            "Synthesize the retrieved information into a concise and coherent response "
            "based on the user query: {query}."
            "Include the source of all retrieved content at the bottom of your response."
            "If the retrieved content is from the PDF, include the source filename and page number."
            "If the retrieved content is from the Web search, include the source url."
            "If you are not able to retrieve the "
            'information then respond with "I\'m sorry, I couldn\'t find the information '
            'you\'re looking for."'
        ),
        backstory=(
            "You're a skilled communicator with a knack for turning "
            "complex information into clear and concise responses."
        ),
        verbose=True,
        llm=load_llm()
    )

    retrieval_task = Task(
        description=(
            "Retrieve the most relevant information from the available "
            "sources for the user query: {query} along with the metadata like source, page number, url."
        ),
        expected_output=(
            "The most relevant information in the form of text as retrieved "
            "from the sources along with the metadata like source, page number, url."
        ),
        agent=retriever_agent
    )

    response_task = Task(
        description="Synthesize the final response for the user query: {query}",
        expected_output=(
            "A concise and coherent response in a well structured markdown format based on the retrieved information "
            "from the right source for the user query: {query} with clear source attribution"
            "(document name and page number, or url as applicable). "
            "**Source attribution is important to maintain credibility.**"
            "If you are not able to retrieve the information, then respond with: "
            '"I am sorry, I could not find the information you are looking for."'
        ),
        agent=response_synthesizer_agent
    )

    crew = Crew(
        agents=[retriever_agent, response_synthesizer_agent],
        tasks=[retrieval_task, response_task],
        process=Process.sequential, 
        verbose=True
    )
    return crew

# ===========================
#   Streamlit Setup
# ===========================

if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0  # Unique key for file uploader

if "messages" not in st.session_state:
    st.session_state.messages = []  # Chat history

if "pdf_tool" not in st.session_state:
    st.session_state.pdf_tool = None  # Store the DocumentSearchTool

if "crew" not in st.session_state:
    st.session_state.crew = None      # Store the Crew object

def reset_chat():
    st.session_state.messages = []
    gc.collect()

def display_pdf(file_bytes: bytes, file_name: str):
    """Displays the uploaded PDF in an iframe."""
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = f"""
    <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" 
        height="600px" 
        type="application/pdf"
    >
    </iframe>
    """
    st.markdown(f"### Preview of {file_name}")
    st.markdown(pdf_display, unsafe_allow_html=True)

# ===========================
#   Sidebar
# ===========================
with st.sidebar:

    if st.button("Reset Session"):
        reset_chat()
        st.session_state.pdf_tool = None
        st.session_state.crew = None 
        st.session_state.file_uploader_key += 1

    st.header("Add Your PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key=st.session_state.file_uploader_key)



    if uploaded_file is not None:
        # If there's a new file and we haven't set pdf_tool yet...
        if st.session_state.pdf_tool is None:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                with st.spinner("Indexing PDF... Please wait..."):
                    st.session_state.pdf_tool = DocumentSearchTool(file_path=temp_file_path)
            
            st.success("PDF indexed! Ready to chat.")

        # Optionally display the PDF in the sidebar
        display_pdf(uploaded_file.getvalue(), uploaded_file.name)

# ===========================
#   Main Chat Interface
# ===========================
st.markdown("""
    # Agentic RAG powered by Gemini""", unsafe_allow_html=True)

# Render existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask a question about your PDF...")

if prompt:
    # 1. Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Build or reuse the Crew (only once after PDF is loaded)
    if st.session_state.crew is None:
        st.session_state.crew = create_agents_and_tasks(st.session_state.pdf_tool)

    # 3. Get the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get the complete response first
        with st.spinner("Thinking..."):
            inputs = {"query": prompt}
            result = st.session_state.crew.kickoff(inputs=inputs)
            full_response = str(result)
        
        # Show the final response without the cursor
        message_placeholder.markdown(full_response)

    # 4. Save assistant's message to session
    st.session_state.messages.append({"role": "assistant", "content": full_response})
