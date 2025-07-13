
# 🤖 Agentic RAG using CrewAI

A powerful Retrieval-Augmented Generation (RAG) system built with CrewAI that intelligently searches through documents and falls back to web search when needed. 

## 🌟 Features

- 📚 Document-based search with RAG capabilities
- 🌐 Automatic fallback to web search
- 🔄 Seamless integration with CrewAI
- 💨 Fast and efficient document processing
- 🎯 Precise answer synthesis with proper source attribution

## 🔄 System Flow

Below is the detailed flow diagram of how the system processes queries and generates responses:

```mermaid
graph TD
    A[Start] --> B[Initialize Streamlit App]
    B --> C[Load LLM Model]
    C --> D[Initialize Session State]
    
    D --> E{PDF Uploaded?}
    E -->|Yes| F[Create DocumentSearchTool]
    E -->|No| G[Wait for PDF Upload]
    
    F --> H[Index PDF Document]
    H --> I[Create Crew]
    
    I --> J[Create Retriever Agent]
    I --> K[Create Response Synthesizer Agent]
    
    J --> L[Add Tools to Retriever Agent]
    L --> L1[PDF Search Tool]
    L --> L2[Web Search Tool]
    
    K --> M[Configure Response Agent]
    
    J & K --> N[Create Tasks]
    N --> N1[Retrieval Task]
    N --> N2[Response Task]
    
    N --> O[User Enters Query]
    
    O --> P[Process Query]
    P --> Q[Show User Message]
    Q --> R[Crew Kickoff]
    
    R --> S[Sequential Processing]
    S --> T1[Retriever Agent Searches]
    T1 --> T2[Response Agent Synthesizes]
    
    T2 --> U[Stream Response]
    U --> V[Update Chat History]
    
    V --> W[Wait for Next Query]
    W --> O
```

## 🚀 Prerequisites

Before running the application, ensure you have:

1. **API Keys**:
   - SERPER API key for web search capabilities
   - LLM API key (if required for your chosen model)

2. **Python Environment**:
   - Python 3.12 or later
   - Conda (recommended for environment management)

## 💻 Installation

1. **Create and Activate Environment**:

   ```bash
   conda create -n crewenv python==3.12 -y
   conda activate crewenv
   ```

2. **Install Dependencies**:

   ```bash
   
   # Install packages
   pip install -r requirements.txt 

   ```

## 🎮 Running the Application

Choose your preferred LLM model:

  ```bash
  streamlit run app.py
  ```

## 🛠️ System Architecture

The system consists of two main agents:

1. **Retriever Agent**:
   - Handles document searching
   - Manages web search fallback
   - Uses both PDF and web search tools

2. **Response Synthesizer Agent**:
   - Processes retrieved information
   - Generates coherent responses
   - Ensures context relevance

## 📚 Usage Examples

1. **Document Search**:
   - Upload your PDF document
   - Enter your query
   - Receive contextual answers from the document

2. **Web Search Fallback**:
   - System automatically detects when document search isn't sufficient
   - Seamlessly switches to web search
   - Combines information from multiple sources


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ArunSubramanian456/CrewAI_Projects/blob/main/3_Agentic_Rag/License.md) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewai) for the amazing framework
- The open-source community for various tools and libraries used in this project

- [Sourangshu Pal's GitHub repo](https://github.com/sourangshupal/agentic_rag_crewai/tree/main)

