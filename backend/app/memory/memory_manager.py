'''This is memory manger we will use right now lanngraph memory module to store memory of agent but in future we will use datastores to store it in sql db , datastore will help to fetch relavant memory for a perticular conversation and based on that it will help to generate response'''
from app.database.database import SessionLocal
from app.models.chat_message import ChatMessage

class MemoryManager:
    def add_message(self, session_id, role, content):
        """
        Adds a new message to the database for the given session.
        """
        db = SessionLocal()
        try:
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content
            )
            db.add(message)
            db.commit()
        finally:
            db.close()  # Ensures the connection is returned to the pool

    def get_history(self, session_id, limit=50):
        """
        Retrieves the chat history for a session, oldest first, limited to N messages.
        """
        db = SessionLocal()
        try:
            messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at.asc())
                .limit(limit)
                .all()
            )
            # Convert the ORM objects to dicts using the model's helper method
            return [msg.to_llm_dict() for msg in messages]
        finally:
            db.close()

    def clear_session(self, session_id):
        """
        Deletes all messages associated with a specific session ID.
        """
        db = SessionLocal()
        try:
            # Execute a bulk delete for efficiency
            db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
            db.commit()
        finally:
            db.close()