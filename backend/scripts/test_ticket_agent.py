import sys
from pathlib import Path

# Add backend directory to sys.path so 'app' module can be found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.ticket_agent import TicketAgent


ticket_agent = TicketAgent()

question = "What is the status of ticket #3?"

print(
    ticket_agent.run(
        question=question,
        session_id="test"
    )
)