# Prompt for routing user queries to the correct agent
# TODO: Refine few-shot examples for production routing.

ROUTER_PROMPT = """
You are an intelligent router. Classify the user query into one of the following categories:
- Technical Support
- Billing
- General Inquiry
"""
