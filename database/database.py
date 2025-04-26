from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from api.model import Base, Clan, ClanSQL
from utils.config import SQLALCHEMY_DATABASE_URL

# Create the engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initialize the database, creating tables if they don't exist and seeding if the database is empty.
    """
    try:
        # Create the tables in the database if they don't exist
        Base.metadata.create_all(bind=engine)
        print("Database tables created or already exist.")
        
        # Check if the 'clans' table is empty
        db = SessionLocal()
        clan_count = db.query(ClanSQL).count()

        if clan_count == 0:
            print("Database is empty. Seeding the database...")
            from database.seeds import seed_database  # Importing seed_database here to avoid circular import
            seed_database()  # Call the seed function to populate the database with initial data
        else:
            print(f"Database already contains {clan_count} clans. Skipping seed.")
        db.close()  # Close the session
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

def load_clans(db: Session):
    """
    Load all clans from the database.
    """
    try:
        clans = db.query(ClanSQL).all()
        print(f"Loaded {len(clans)} clans from the database.")
        return clans
    except Exception as e:
        print(f"Error loading clans: {e}")
        return []

def save_clans(db: Session, clan: ClanSQL):
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
