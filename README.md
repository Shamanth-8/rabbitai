# Code Bunny - AI-Powered Code Analysis Tool

A smart coding assistant that analyzes your Python code and provides AI-powered insights and interactive chat support.

## Features

- **Static Code Analysis**: Analyzes code complexity, maintainability, and function structure
- **AI Insights**: Get personalized code improvement suggestions based on your skill level
- **Interactive Chat**: Talk to Code Bunny 🐇 for coding help and explanations
- **Skill Level Adaptation**: Tailored feedback for different experience levels

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# Copy the example file
cp env_example.txt .env

# Edit .env and add your Google Gemini API key
GOOGLE_API_KEY=your_actual_api_key_here
```

**Get your API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run the Application

#### Start the Backend (FastAPI)
```bash
# Option 1: Using the improved startup script
python start_backend.py

# Option 2: Using the basic script
python run_backend.py

# Option 3: Windows users can double-click
start_backend.bat
```
The backend will run on http://127.0.0.1:8000

#### Start the Frontend (Streamlit)
```bash
# Option 1: Using the improved startup script
python start_frontend.py

# Option 2: Using the basic script
python run_frontend.py

# Option 3: Windows users can double-click
start_frontend.bat
```
The frontend will run on http://127.0.0.1:8501

**Important:** Start the backend first, then the frontend!

## Usage

1. **Upload Your Code**: Upload a Python file (.py) or text file (.txt)
2. **Describe the Problem**: Explain what you're trying to solve
3. **Choose Your Level**: Select your experience level for personalized feedback
4. **Get Analysis**: Submit for static analysis and AI insights
5. **Chat with Code Bunny**: Ask questions and get help with your code

## Project Structure

```
rabbitai/
├── backend/
│   ├── app.py          # FastAPI server
│   ├── analyzer.py     # Code analysis logic
│   └── ai_helper.py    # AI integration
├── frontend/
│   └── streamlit_app.py # Streamlit UI
├── requirements.txt     # Python dependencies
├── run_backend.py      # Backend startup script
├── run_frontend.py     # Frontend startup script
└── env_example.txt     # Environment variables template
```

## API Endpoints

- `POST /analyze` - Analyze uploaded code
- `POST /code-bunny` - Chat with Code Bunny

## live demo -- https://code-bunny-frontend-gozt.onrender.com/

## Requirements

- Python 3.8+
- Google Gemini API key
- Internet connection for AI feature
