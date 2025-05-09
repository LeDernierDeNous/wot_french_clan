from database.database import save_clans, SessionLocal
from utils.config import SEED_DATA_PATH
import json
import os
from api.model import ClanSQL
from utils.logging import setup_logger

# Set up the logger for this file/module
logger = setup_logger(__name__)

def load_seed_data(seed_file_path):
    """
    Loads the seed data from a JSON file.
    """
    if not os.path.exists(seed_file_path):
        logger.error(f"Seed file not found: {seed_file_path}")
        raise FileNotFoundError(f"Seed file not found: {seed_file_path}")

    with open(seed_file_path, 'r', encoding='utf-8') as f:
        logger.info(f"Successfully loaded seed data from {seed_file_path}.")
        return json.load(f)

def seed_database():
    """
    Seeds the database with the clans from the seed file.
    """
    db = SessionLocal()  # Create a database session

    try:
        seed_clans = load_seed_data(SEED_DATA_PATH)

        logger.info(f"Starting to seed database with {len(seed_clans)} clans...")

        for clan_data in seed_clans:
            clan = ClanSQL(
                id=clan_data['clan_id'],
                clan_tag=clan_data['clan_tag'],
                clan_name=clan_data['clan_name'],
                country=clan_data.get('country', "Unknown")
            )
            save_clans(db, clan)  # Pass the db session to save_clans()

        logger.info(f"✅ Successfully seeded database with {len(seed_clans)} clans.")

    except Exception as e:
        logger.error(f"❌ Error while seeding the database: {str(e)}")

    finally:
        db.close()  # Ensure the db session is closed after seeding
