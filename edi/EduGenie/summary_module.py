import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def summarize_text(text: str) -> str:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    prompt = f"""
Summarize the following educational passage for quick revision.

Rules:
- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Prefer short paragraphs or bullet points.
- Do not add information that is not in the passage.

Passage:
{text}
"""

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return response.text.strip()
