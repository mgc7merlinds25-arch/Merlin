import json
import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=key)


def clean_json_block(text: str) -> str:
    """Remove Markdown fences and surrounding text around a JSON array."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        text = text[start:end + 1]
    return text.strip()


def generate_quiz(passage: str):
    prompt = f"""
Create exactly 3 multiple-choice questions from the educational passage below.

Return ONLY valid JSON in this exact structure:
[
  {{
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A"
  }}
]

Requirements:
- Exactly 3 questions.
- Exactly 4 options per question.
- One correct answer per question.
- Questions must be answerable from the supplied passage.
- Do not add Markdown or commentary.

Passage:
{passage}
"""

    response = _client().models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )

    raw = response.text.strip()
    try:
        data = json.loads(clean_json_block(raw))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Quiz JSON parsing failed: {exc}") from exc

    if not isinstance(data, list) or len(data) != 3:
        raise RuntimeError("The AI did not return exactly 3 quiz questions.")

    for item in data:
        if not all(k in item for k in ("question", "options", "correct_answer")):
            raise RuntimeError("Invalid quiz item returned by the AI.")
        if not isinstance(item["options"], list) or len(item["options"]) != 4:
            raise RuntimeError("Each quiz question must have exactly 4 options.")

    return data
