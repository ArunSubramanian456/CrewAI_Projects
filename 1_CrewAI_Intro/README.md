# AI Content Research & Writing Assistant

A powerful content generation system built with CrewAI that combines research, analysis, and writing capabilities to produce high-quality blog posts on any topic.

## 🚀 Features

- Automated research using SerpDev tool
- AI-powered content writing and analysis
- Streamlit web interface for easy interaction
- Downloadable markdown output

## 📋 Prerequisites

- Python 3.12
- Gemini API key
- SerperDev API key

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CrewAI-Demo
```

2. Create and activate a virtual environment:
```bash
conda create -n crewai python==3.12 -y
conda activate crewai
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys to `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_key
```

## 🚀 Running the Application

### Command Line Version
Run the basic version using:
```bash
python app.py
```

### Web Interface
Launch the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```
Then open your browser and navigate to `http://localhost:8501`

## 💻 Usage

1. **Web Interface**:
   - Enter your desired topic in the sidebar
   - Adjust the temperature setting if needed
   - Click "Generate Content"
   - Wait for the AI to generate your article
   - Download the result as a markdown file

2. **Command Line**:
   - Edit the topic in `app.py`
   - Run the script
   - Results will be printed to console

## 🔧 Project Structure

```
ai-content-assistant/
├── streamlit_app.py    # Web interface
├── app.py             # Command line version
├── requirements.txt   # Project dependencies
├── .env              # Environment variables
└── README.md         # Documentation
```




