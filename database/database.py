from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.model import Base, Clan
from api.config import DATABASE_URL

# Create an engine to manage the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # check_same_thread=False for SQLite

# Create a sessionmaker to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database, creating tables if they don't exist.
    """
    # Create the tables in the database if they don't exist
    Base.metadata.create_all(bind=engine)

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
    return db.query(Clan).all()

def save_clans(db, clan: Clan):
    """
    Save a clan to the database.
    """
    db.add(clan)
    db.commit()
    db.refresh(clan)
    return clan
