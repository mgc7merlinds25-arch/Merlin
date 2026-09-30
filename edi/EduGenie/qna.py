import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. Add it to your .env file."
    )


def answer_question(question: str) -> str:
    question = question.strip()

    if not question:
        return "Please enter a question."

    prompt = f"""
You are EduGenie, an educational assistant.
Answer the student's question accurately and clearly.

Question:
{question}

Rules:
- Use simple language.
- Give the direct answer first.
- Add short bullet points when useful.
- If the question is academic, include a small example when appropriate.
- Do not invent facts.
"""

    # Create a fresh Gemini client for this request
    client = genai.Client(api_key=API_KEY)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2
            ),
        )

        if response.text:
            return response.text.strip()

        return "Sorry, I couldn't generate an answer."

    finally:
        client.close()