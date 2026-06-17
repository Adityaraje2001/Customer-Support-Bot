from app.prompts.router_prompt import ROUTER_PROMPT


class RouterAgent:

    def __init__(self, llm_service):
        self.llm_service = llm_service

    def route(
        self,
        question: str
    ):
        prompt = f"""
        {ROUTER_PROMPT}

        User Question:
        {question}
        """

        route = self.llm_service.get_response(
            prompt
        )

        return route.strip().lower()