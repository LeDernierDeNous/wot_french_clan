from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.model import Base, Clan
from api.config import SQLALCHEMY_DATABASE_URL

# Create the engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database, creating tables if they don't exist.
    """
    try:
        # Create the tables in the database if they don't exist
        Base.metadata.create_all(bind=engine)
        print("Database tables created or already exist.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise

def get_db():
    """
    Get a database session for FastAPI dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_clans(db):
    """
    Load all clans from the database.
    """
    try:
        clans = db.query(Clan).all()
        print(f"Loaded {len(clans)} clans from the database.")
        return clans
    except Exception as e:
        print(f"Error loading clans: {e}")
        return []

def save_clans(db, clan: Clan):
    """
    Save a clan to the database.
    """
    try:
        db.add(clan)
        db.commit()
        db.refresh(clan)
        print(f"Clan {clan.clan_name} saved successfully.")
        return clan
    except Exception as e:
        print(f"Error saving clan: {e}")
        db.rollback()
        return None
