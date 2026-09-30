import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_learning_recommendations(topic: str) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
Create a personalized learning path for the topic: {topic}

Organize it from beginner to advanced.

Include:
1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Suggested order of learning
5. A simple timeline
6. Useful resource types such as videos, articles, documentation, or books
7. A small practice/project suggestion

Keep it practical and easy for a student to follow.
"""

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.4),
    )
    return response.text.strip()
