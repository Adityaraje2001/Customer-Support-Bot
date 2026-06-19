import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the backend directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import Base
from app.models.user import User
from app.models.ticket import Ticket
from app.models.chat_message import ChatMessage

def migrate():
    # 1. Setup environment
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    
    # 2. Connect to old SQLite database
    sqlite_url = "sqlite:///./data/app.db"
    sqlite_engine = create_engine(sqlite_url)
    SqliteSession = sessionmaker(bind=sqlite_engine)
    
    # 3. Connect to new Postgres database
    pg_url = os.getenv("DATABASE_URL")
    if not pg_url or pg_url.startswith("sqlite"):
        print("Error: DATABASE_URL must be set to a Postgres URL in .env")
        sys.exit(1)
        
    pg_engine = create_engine(pg_url)
    
    # 4. Create tables in PostgreSQL
    print("Creating tables in PostgreSQL...")
    Base.metadata.create_all(bind=pg_engine)
    PgSession = sessionmaker(bind=pg_engine)
    
    # 5. Migrate data
    print("Starting data migration...")
    with SqliteSession() as sqlite_session:
        with PgSession() as pg_session:
            # Users
            users = sqlite_session.query(User).all()
            print(f"Found {len(users)} users to migrate.")
            for user in users:
                sqlite_session.expunge(user)
                pg_session.merge(user)
            
            # Tickets
            tickets = sqlite_session.query(Ticket).all()
            print(f"Found {len(tickets)} tickets to migrate.")
            for ticket in tickets:
                sqlite_session.expunge(ticket)
                pg_session.merge(ticket)
                
            # ChatMessages
            messages = sqlite_session.query(ChatMessage).all()
            print(f"Found {len(messages)} chat messages to migrate.")
            for message in messages:
                sqlite_session.expunge(message)
                pg_session.merge(message)
                
            try:
                pg_session.commit()
                print("✅ Migration completed successfully!")
            except Exception as e:
                pg_session.rollback()
                print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
