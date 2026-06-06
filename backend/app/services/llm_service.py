""" This is where the LLM interacts with the user."""
from groq import Groq
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class LLMService:
    """Handles communication with Groq LLM."""

    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("GROQ_MODEL")

        if not self.model:
            raise ValueError("GROQ_MODEL not found")

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def get_response(self, message: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"Groq API Error: {str(e)}")