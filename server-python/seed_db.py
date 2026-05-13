import os
import json
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL environment variable is not set!")
        return None
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    try:
        return create_engine(db_url)
    except Exception as e:
        logger.error(f"Error creating database engine: {e}")
        return None

def seed_database():
    engine = get_db_engine()
    if not engine:
        return

    # Dummy Data
    users = [
        {"id": "user_dev", "interests": json.dumps(["Web Development", "React", "JavaScript"])},
        {"id": "user_ml", "interests": json.dumps(["Machine Learning", "AI", "PyTorch", "Python"])},
        {"id": "user_speaker", "interests": json.dumps(["Public Speaking", "Debate", "Leadership"])},
        {"id": "user_mixed", "interests": json.dumps(["Python", "Web Development", "AI"])},
        {"id": "user_hardware", "interests": json.dumps(["Robotics", "IoT", "C++"])},
        {"id": "101", "interests": json.dumps(["web", "react"])}
    ]

    events = [
        {"id": "evt_1", "name": "React Masterclass Workshop", "date_text": "2026-06-01", "description": "Learn React from scratch.", "tags": json.dumps(["Web Development", "React", "JavaScript"])},
        {"id": "evt_2", "name": "PyTorch Hackathon 2026", "date_text": "2026-06-15", "description": "Build ML models in 48 hours.", "tags": json.dumps(["Machine Learning", "AI", "PyTorch", "Python"])},
        {"id": "evt_3", "name": "National Debate Competition", "date_text": "2026-07-10", "description": "Showcase your speaking skills.", "tags": json.dumps(["Public Speaking", "Debate"])},
        {"id": "evt_4", "name": "Fullstack Web Bootcamp", "date_text": "2026-07-20", "description": "MERN stack basics.", "tags": json.dumps(["Web Development", "Node.js", "React"])},
        {"id": "evt_5", "name": "AI Ethics Seminar", "date_text": "2026-08-05", "description": "Discussing the future of AI.", "tags": json.dumps(["AI", "Public Speaking", "Machine Learning"])},
        {"id": "evt_6", "name": "IoT and Robotics Expo", "date_text": "2026-08-15", "description": "Explore the latest in hardware.", "tags": json.dumps(["Robotics", "IoT", "Hardware"])},
        {"id": "evt_7", "name": "Leadership Summit", "date_text": "2026-09-01", "description": "Building the leaders of tomorrow.", "tags": json.dumps(["Leadership", "Public Speaking"])},
        {"id": "evt_8", "name": "Python for Data Science", "date_text": "2026-09-10", "description": "Data analysis using Pandas.", "tags": json.dumps(["Python", "Machine Learning", "Data"])},
        {"id": "evt_9", "name": "Frontend UI/UX Hackathon", "date_text": "2026-09-25", "description": "Design meets code.", "tags": json.dumps(["Web Development", "React", "UI/UX"])},
        {"id": "evt_10", "name": "C++ Game Engine Dev", "date_text": "2026-10-05", "description": "Build your own engine.", "tags": json.dumps(["C++", "Hardware"])}
    ]

    # Let's create a scenario for collaborative filtering:
    # user_ml and user_mixed both like AI/Python. user_ml joined evt_2 and evt_8.
    # Therefore, evt_8 should get a collaborative boost for user_mixed.
    participations = [
        {"user_id": "user_dev", "event_id": "evt_1"},
        {"user_id": "user_dev", "event_id": "evt_4"},
        {"user_id": "user_ml", "event_id": "evt_2"},
        {"user_id": "user_ml", "event_id": "evt_8"},
        {"user_id": "user_mixed", "event_id": "evt_2"}, # Joined one event in common with user_ml
        {"user_id": "user_speaker", "event_id": "evt_3"},
        {"user_id": "user_hardware", "event_id": "evt_6"},
        {"user_id": "user_hardware", "event_id": "evt_10"}
    ]

    with engine.connect() as conn:
        with conn.begin():
            logger.info("Ensuring tables exist...")
            
            # Create user_profiles table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id TEXT PRIMARY KEY,
                    interests JSONB NOT NULL DEFAULT '[]'::jsonb
                );
            """))

            # Create event_participants table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS event_participants (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    event_id TEXT NOT NULL,
                    UNIQUE(user_id, event_id)
                );
            """))

            # Clean existing dummy data to avoid duplicates if run multiple times
            conn.execute(text("DELETE FROM event_participants"))
            conn.execute(text("DELETE FROM user_profiles"))
            
            # Since events might have other actual data, we will just upsert
            
            logger.info("Inserting Users...")
            for u in users:
                conn.execute(text("""
                    INSERT INTO user_profiles (id, interests)
                    VALUES (:id, :interests::jsonb)
                    ON CONFLICT (id) DO UPDATE SET interests = EXCLUDED.interests
                """), u)

            logger.info("Inserting Events...")
            for e in events:
                conn.execute(text("""
                    INSERT INTO events (id, name, date_text, description, status, tags)
                    VALUES (:id, :name, :date_text, :description, 'upcoming', :tags::jsonb)
                    ON CONFLICT (id) DO UPDATE SET 
                        name = EXCLUDED.name, 
                        tags = EXCLUDED.tags,
                        description = EXCLUDED.description
                """), e)

            logger.info("Inserting Event Participations...")
            for p in participations:
                conn.execute(text("""
                    INSERT INTO event_participants (user_id, event_id)
                    VALUES (:user_id, :event_id)
                    ON CONFLICT DO NOTHING
                """), p)

    logger.info("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
