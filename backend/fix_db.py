import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")
    
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from app.models.document import Document
from app.models.user import User  # Needed for foreign key resolution

db = SessionLocal()
try:
    stuck_docs = db.query(Document).filter(Document.status == 'processing').all()
    for doc in stuck_docs:
        doc.status = 'failed'
        doc.error_message = 'Failed due to worker deadlock. Please delete and re-upload.'
    db.commit()
    print(f"Updated {len(stuck_docs)} documents from processing to failed.")
finally:
    db.close()
