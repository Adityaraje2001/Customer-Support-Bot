class EscalationAgent:

    def __init__(self, llm_service=None):
        self.llm_service = llm_service

    def run(
        self,
        question: str,
        history=None
    ):
        return (
            "Your request has been escalated "
            "to a human support representative."
        )