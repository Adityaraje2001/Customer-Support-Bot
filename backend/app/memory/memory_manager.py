'''This is memory manger we will use right now lanngraph memory module to store memory of agent but in future we will use datastores to store it in sql db , datastore will help to fetch relavant memory for a perticular conversation and based on that it will help to generate response'''
from app.database.database import SessionLocal
from app.models.chat_message import ChatMessage

class MemoryManager:
    def add_message(self, session_id, role, content, user_id=None, message_id=None):
        """
        Adds a new message to the database for the given session.
        """
        db = SessionLocal()
        try:
            kwargs = dict(
                session_id=session_id,
                role=role,
                content=content,
                user_id=user_id,
            )
            if message_id is not None:
                kwargs["id"] = message_id

            message = ChatMessage(**kwargs)
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

    def get_conversations_for_user(self, user_id):
        """
        Retrieves a list of unique conversations for a user, ordered by most recent message.
        """
        db = SessionLocal()
        try:
            from sqlalchemy import func
            
            # Find the most recent message time for each session
            subq = (
                db.query(
                    ChatMessage.session_id,
                    func.max(ChatMessage.created_at).label('last_updated')
                )
                .filter(ChatMessage.user_id == user_id)
                .group_by(ChatMessage.session_id)
                .subquery()
            )
            
            # Join to get the first message (to use as title)
            # A simple approach is just to get all sessions and then process in python
            messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.user_id == user_id)
                .order_by(ChatMessage.created_at.asc())
                .all()
            )
            
            conversations = {}
            for msg in messages:
                content_str = str(msg.content)
                if msg.session_id not in conversations:
                    conversations[msg.session_id] = {
                        "id": msg.session_id,
                        "title": content_str[:50] + "..." if len(content_str) > 50 else content_str,
                        "createdAt": msg.created_at.isoformat(),
                        "updatedAt": msg.created_at.isoformat(),
                        "messageCount": 0,
                        "messages": []
                    }
                conv = conversations[msg.session_id]
                conv["updatedAt"] = msg.created_at.isoformat()
                conv["messageCount"] += 1
                conv["messages"].append({
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat(),
                    "agentUsed": None # Assuming no agent used info in db currently
                })
            
            # Sort by updatedAt descending
            result = list(conversations.values())
            result.sort(key=lambda x: x["updatedAt"], reverse=True)
            return result
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