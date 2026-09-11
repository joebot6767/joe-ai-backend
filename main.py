import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI


app = FastAPI(title="JOE AI Backend")


# Allow your GitHub Pages website to communicate with this server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "service": "JOE AI Backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return {
            "error": "OPENAI_API_KEY is not configured on the server."
        }

    try:

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model="gpt-5.6-mini",
            instructions=(
                "You are JOE, a helpful AI assistant. "
                "Be friendly, clear and useful. "
                "Answer the user's question directly."
            ),
            input=request.message
        )

        return {
            "reply": response.output_text
        }

    except Exception as error:

        return {
            "error": "The AI service could not be reached.",
            "details": str(error)
        }

