import sys
from pathlib import Path

# Add backend directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from app.database.database import engine
from sqlalchemy import text

def migrate():
    with engine.begin() as conn:
        print("Starting migration...")
        
        # Add new columns if they don't exist
        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN processing_started_at TIMESTAMP WITH TIME ZONE;"))
            print("Added processing_started_at column.")
        except Exception as e:
            print(f"Skipping processing_started_at: {e}")

        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN processing_completed_at TIMESTAMP WITH TIME ZONE;"))
            print("Added processing_completed_at column.")
        except Exception as e:
            print(f"Skipping processing_completed_at: {e}")

        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN error_message VARCHAR;"))
            print("Added error_message column.")
        except Exception as e:
            print(f"Skipping error_message: {e}")

        # Change default value of status
        try:
            conn.execute(text("ALTER TABLE documents ALTER COLUMN status SET DEFAULT 'pending';"))
            print("Changed status default to 'pending'.")
        except Exception as e:
            print(f"Skipping default change: {e}")

        print("Migration complete.")

if __name__ == "__main__":
    migrate()
