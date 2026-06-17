from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
import os
from app.services.llm_service import LLMService
from app.api.router import router

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
app = FastAPI(
    title="AI Customer Support Agent API",
    description="Backend API for AI Customer Support Agent",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Customer Support Agent API"}

@app.on_event("startup")
def on_startup():
    from app.database.database import Base, engine
    from app.models.ticket import Ticket  # noqa: F401 — registers model with Base
    from app.models.chat_message import ChatMessage  # noqa: F401 — registers model with Base
    Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="[IP_ADDRESS]", port=8000)
