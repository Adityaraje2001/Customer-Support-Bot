import json
import logging
from app.services.llm_service import LLMService
from app.evaluation.prompts import EVALUATION_PROMPT

logger = logging.getLogger(__name__)

class ResponseEvaluator:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    def evaluate(self, question: str, answer: str, retrieved_context: str, route_selected: str) -> dict[str, int]:
        default_scores = {
            "answer_relevance": 3,
            "context_relevance": 3,
            "groundedness": 3,
            "hallucination_risk": 3,
            "route_accuracy": 3
        }
        
        try:
            prompt = EVALUATION_PROMPT.format(
                question=question,
                answer=answer,
                retrieved_context=retrieved_context,
                route_selected=route_selected
            )
            
            response_text = self.llm_service.get_response(prompt)
            
            # Clean the response text in case it contains markdown
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
                
            scores = json.loads(clean_text)
            
            # Validate each score is an int between 1 and 5
            validated_scores = {}
            for key in default_scores.keys():
                val = scores.get(key, 3)
                if isinstance(val, (int, float)):
                    val = int(val)
                    if 1 <= val <= 5:
                        validated_scores[key] = val
                    else:
                        validated_scores[key] = max(1, min(5, val))
                else:
                    validated_scores[key] = 3
            return validated_scores
            
        except Exception as e:
            logger.warning("Evaluation failed, using default scores. Error: %s", e)
            return default_scores
