import os
from dotenv import load_dotenv

load_dotenv()

# The project document describes LaMini-Flan-T5 as the lightweight
# concept-explanation model. This implementation uses it when available
# and falls back to Gemini so the application remains easy to run.

_pipeline = None


def _get_local_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    try:
        from transformers import pipeline
        _pipeline = pipeline(
            "text2text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M",
        )
        return _pipeline
    except Exception:
        return None


def explain_topic(topic: str) -> str:
    prompt = (
        "Explain the following educational topic in simple language. "
        "Give a short definition, key points, and one simple example.\n\n"
        f"Topic: {topic}"
    )

    local = _get_local_pipeline()
    if local is not None:
        try:
            result = local(prompt, max_new_tokens=220, do_sample=False)
            if result and result[0].get("generated_text"):
                return result[0]["generated_text"].strip()
        except Exception:
            pass

    # Fallback to Gemini if the local model is unavailable.
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return (
            "The local explanation model is not available, and GEMINI_API_KEY "
            "is not configured. Install the local model dependencies or add "
            "your Gemini API key."
        )

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.2),
    )
    return response.text.strip()
