import os
import json
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import httpx

# ---------------- LOGGING SETUP ----------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------- LOAD ENV ----------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

# ---------------- CONSTANTS ----------------
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
CHAT_HISTORY_FILE = "chat_history.json"
MAX_CHAT_HISTORY = 100

# ---------------- APP SETUP ----------------
app = FastAPI(title="AI Chatbot", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- HELPER FUNCTIONS ----------------
def get_current_time() -> str:
    return datetime.now().strftime("%d %b %Y, %I:%M %p")

def format_ai_response(text: str) -> str:
    return text.strip()

# ---------------- AI FUNCTION ----------------
async def ask_ai(user_message: str, chat: List[Dict[str, str]]) -> str:
    headers = {
        "Content-Type": "application/json"
    }

    # ---- BUILD CONTEXT (LAST 6 MESSAGES) ----
    contents = []
    for msg in chat[-6:]:
        contents.append({
            "parts": [
                {"text": f"{msg['sender']}: {msg['message']}"}
            ]
        })

    # Add current user message
    contents.append({
        "parts": [
            {"text": f"You: {user_message}"}
        ]
    })

    payload = {
        "contents": contents
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={API_KEY}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

        # ---- SAFE PARSING FOR GEMINI 2.5 ----
        candidates = result.get("candidates")
        if not candidates:
            logger.error(f"No candidates: {result}")
            return "⚠️ AI did not return a response."

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])

        if not parts or "text" not in parts[0]:
            logger.error(f"No text in response: {result}")
            return "⚠️ AI response was empty."

        return parts[0]["text"].strip()

    except httpx.TimeoutException:
        logger.error("Gemini timeout")
        return "⚠️ Request timed out."

    except httpx.HTTPStatusError as e:
        logger.error(f"Gemini HTTP error: {e.response.text}")
        return "⚠️ AI service error."

    except Exception:
        logger.exception("Unexpected Gemini error")
        return "⚠️ Something went wrong."

# ---------------- CHAT STORAGE ----------------
def load_chat_history() -> List[Dict[str, str]]:
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []

    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_chat_history(chat: List[Dict[str, str]]) -> None:
    if len(chat) > MAX_CHAT_HISTORY:
        chat = chat[-MAX_CHAT_HISTORY:]

    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(chat, f, indent=2, ensure_ascii=False)

def clear_chat_history() -> None:
    if os.path.exists(CHAT_HISTORY_FILE):
        os.remove(CHAT_HISTORY_FILE)

# ---------------- ROUTES ----------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    chat = load_chat_history()
    return templates.TemplateResponse(
        "page.html",
        {"request": request, "chat": chat}
    )

# ✅ FIXED POST ROUTE (THIS WAS THE BUG)
@app.post("/", response_class=HTMLResponse)
async def chat_message(request: Request, message: Optional[str] = Form(None)):
    chat = load_chat_history()

    # ---- CRITICAL FIX ----
    if not message:
        logger.warning("Message missing or empty")
        return templates.TemplateResponse(
            "page.html",
            {"request": request, "chat": chat}
        )

    message = message.strip()
    if not message:
        return templates.TemplateResponse(
            "page.html",
            {"request": request, "chat": chat}
        )

    if len(message) > 5000:
        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "chat": chat,
                "error": "Message too long (max 5000 characters)"
            }
        )

    ai_response = await ask_ai(message)
    current_time = get_current_time()

    chat.append({
        "sender": "You",
        "message": message,
        "time": current_time
    })

    chat.append({
        "sender": "AI",
        "message": ai_response,
        "time": current_time
    })

    save_chat_history(chat)

    return templates.TemplateResponse(
        "page.html",
        {"request": request, "chat": chat}
    )

from fastapi.responses import JSONResponse

@app.post("/api/chat")
async def chat_api(message: str = Form(...)):
    chat = load_chat_history()

    message = message.strip()
    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)

    ai_response = await ask_ai(message, chat)
    current_time = get_current_time()

    user_msg = {
        "sender": "You",
        "message": message,
        "time": current_time
    }

    ai_msg = {
        "sender": "AI",
        "message": ai_response,
        "time": current_time
    }

    chat.append(user_msg)
    chat.append(ai_msg)
    save_chat_history(chat)

    return {
        "user": user_msg,
        "ai": ai_msg
    }


@app.post("/clear")
async def clear_chat():
    clear_chat_history()
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "time": get_current_time()}

# ---------------- EVENTS ----------------
@app.on_event("startup")
async def startup_event():
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    logger.info("App started")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("App stopped")
