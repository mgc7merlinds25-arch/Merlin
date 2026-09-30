import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

load_dotenv()

app = FastAPI(title="EduGenie - Google Gemini Powered Learning Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": None
        }
    )


@app.post("/qa")
async def qa(request: Request):
    data = await request.json()
    question = str(data.get("question", "")).strip()

    if not question:
        return JSONResponse(
            {"error": "Please enter a question."},
            status_code=400
        )

    return {"answer": answer_question(question)}


@app.post("/explain")
async def explain(request: Request):
    data = await request.json()
    topic = str(data.get("topic", "")).strip()

    if not topic:
        return JSONResponse(
            {"error": "Please enter a topic."},
            status_code=400
        )

    return {"explanation": explain_topic(topic)}


@app.post("/quiz")
async def quiz(request: Request):
    data = await request.json()
    text = str(data.get("text", "")).strip()

    if not text:
        return JSONResponse(
            {"error": "Please enter a topic or passage."},
            status_code=400
        )

    return {"quiz": generate_quiz(text)}


@app.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    text = str(data.get("text", "")).strip()

    if not text:
        return JSONResponse(
            {"error": "Please enter text to summarize."},
            status_code=400
        )

    return {"summary": summarize_text(text)}


@app.post("/learn/recommendations")
async def learn_recommendations(request: Request):
    data = await request.json()
    topic = str(data.get("topic", "")).strip()

    if not topic:
        return JSONResponse(
            {"error": "Please enter a topic."},
            status_code=400
        )

    return {
        "recommendations": get_learning_recommendations(topic)
    }


@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    task: str = Form(...),
    user_input: str = Form(...)
):
    user_input = user_input.strip()

    result = None
    error = None

    try:
        if not user_input:
            error = "Please enter some text."

        elif task == "qa":
            result = answer_question(user_input)

        elif task == "explain":
            result = explain_topic(user_input)

        elif task == "quiz":
            result = generate_quiz(user_input)

        elif task == "summarize":
            result = summarize_text(user_input)

        elif task == "learn":
            result = get_learning_recommendations(user_input)

        else:
            error = "Unknown task."

    except Exception as exc:
        error = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result,
            "error": error,
            "selected_task": task,
            "user_input": user_input,
        }
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        )
    }