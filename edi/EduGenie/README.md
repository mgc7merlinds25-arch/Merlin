# EduGenie - Google Gemini Powered Learning Assistant

## Features
- Question answering
- Simple concept explanations
- 3-question MCQ quiz generation
- Text summarization
- Personalized learning paths
- FastAPI backend
- HTML/CSS frontend

## Project structure

EduGenie/
├── main.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── requirements.txt
├── .env.example
└── README.md

## Setup

1. Install Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies:

   pip install -r requirements.txt

4. Copy `.env.example` to `.env`.
5. Put your Gemini API key in `.env`:

   GEMINI_API_KEY=your_key_here

6. Start the server:

   uvicorn main:app --reload

7. Open:

   http://127.0.0.1:8000

## Notes

The explanation module first attempts to use the LaMini-Flan-T5 model described in the project document. If that local model cannot be loaded, it falls back to Gemini.

Keep your API key private. Do not commit `.env` to a public repository.
