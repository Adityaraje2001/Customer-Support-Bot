"""This is where the LLM interacts with the user."""

from groq import Groq
import os
from dotenv import load_dotenv
from typing import Optional, AsyncGenerator, Any

load_dotenv()


class LLMService:
    """Handles communication with Groq LLM."""

    def __init__(self, model: Optional[str] = None):
        loaded_model = model or os.getenv("GROQ_MODEL")

        if not loaded_model:
            raise ValueError("GROQ_MODEL not found")
            
        self.model: str = loaded_model

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.system_prompt: dict[str, str] = {
            "role" : "system",
            "content" : "You are a helpful assistant."
        }
    # ──────────────────────────────────────────────
    # Helper: Builds the message array with history
    # ──────────────────────────────────────────────
    def _build_messages(self, message: str, history: list[dict] | None = None) -> list[Any]:
        """Constructs the message payload: System Prompt -> History -> Current Message."""
        messages: list[Any] = [self.system_prompt]
        
        if history:
            messages.extend(history)
            
        messages.append({
            "role": "user",
            "content": message
        })
        
        return messages
    # ──────────────────────────────────────────────
    # Non-streaming: returns the full response at once
    # ──────────────────────────────────────────────
    def get_response(self, message: str, history: list[dict] | None = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(message, history)
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            raise Exception(f"Groq API Error: {str(e)}")
    # ──────────────────────────────────────────────
    # Streaming: yields tokens one-by-one as SSE events
    # ──────────────────────────────────────────────
    async def stream_response(self, message: str, history: list[dict] | None = None) -> AsyncGenerator[str, None]:
        """
        Stream a response from Groq token-by-token, including conversation history.
        """
        import json
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self._build_messages(message, history),
                stream=True, 
            )

            for chunk in stream:
                token = chunk.choices[0].delta.content
                if token is not None:
                    yield f"data: {json.dumps(token)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:

            
            yield f"data: [ERROR] {str(e)}\n\n"