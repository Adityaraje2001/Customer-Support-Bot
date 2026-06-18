EVALUATION_PROMPT = """
You are an expert AI response evaluator. Your task is to evaluate the quality of a customer support assistant's response.
Please score the following dimensions on a scale of 1 to 5:

1. **answer_relevance**: How relevant is the answer to the user's question? (1 = completely irrelevant, 5 = perfectly relevant)
2. **context_relevance**: How relevant is the retrieved context to answering the question? (1 = completely irrelevant, 5 = highly relevant)
3. **groundedness**: How well is the answer supported by the retrieved context? (1 = entirely made up, 5 = fully supported)
4. **hallucination_risk**: Are there any facts in the answer not present in the context? (1 = high hallucination risk, 5 = no hallucination)
5. **route_accuracy**: Does the selected route make sense for the question? (1 = completely wrong route, 5 = perfect route)

User Question:
{question}

Assistant Answer:
{answer}

Retrieved Context:
{retrieved_context}

Route Selected:
{route_selected}

Respond STRICTLY with a valid JSON object matching this schema. Do not include markdown formatting or any other text.
{{
    "answer_relevance": int,
    "context_relevance": int,
    "groundedness": int,
    "hallucination_risk": int,
    "route_accuracy": int
}}
"""
