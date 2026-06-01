from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
import os
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = FastAPI(
    title="AI Customer Support Agent API",
    description="Backend API for AI Customer Support Agent",
    version="0.1.0"
)

class HealthCheckResponse(BaseModel):
    status: str
    version: str

@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return HealthCheckResponse(status="ok", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Welcome to AI Customer Support Agent API"}

@app.get("/test")
async def test():
    return {"message":"This is a API Endpoint"}

class LLM_test(BaseModel):
    message:str
    model: str = "llama-3.1-8b-instant" 

@app.post("/test_llm")
async def test_llm(message:LLM_test):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model=message.model,
            messages=[{"role": "user", "content": message.message}],
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}