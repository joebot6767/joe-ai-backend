import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="JOE AI Backend")

Allow the GitHub Pages website to communicate with JOE.

app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_credentials=False,
allow_methods=[""],
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

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    return {
        "error": "GEMINI_API_KEY is not configured."
    }

message = request.message.strip()

if not message:
    return {
        "error": "Message cannot be empty."
    }

try:

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message
    )

    if not response.text:
        return {
            "error": "The AI returned an empty response."
        }

    return {
        "reply": response.text
    }

except Exception as error:

    print("Gemini error:", error)

    return {
        "error": "Gemini could not answer the request.",
        "details": str(error)
    }
