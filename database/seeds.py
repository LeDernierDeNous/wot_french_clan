# database/seeds.py
from database.database import save_clans, SessionLocal
from api.config import SEED_DATA_PATH
import json
import os
from api.model import ClanSQL

def load_seed_data(seed_file_path):
    """
    Loads the seed data from a JSON file.
    """
    if not os.path.exists(seed_file_path):
        raise FileNotFoundError(f"Seed file not found: {seed_file_path}")

    with open(seed_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_database():
    """
    Seeds the database with the clans from the seed file.
    """
    db = SessionLocal()  # Create a database session

    try:
        seed_clans = load_seed_data(SEED_DATA_PATH)

        for clan_data in seed_clans:
            clan = ClanSQL(
                id=clan_data['clan_id'],
                clan_tag=clan_data['clan_tag'],
                clan_name=clan_data['clan_name'],
                country=clan_data.get('country', "Unknown")
            )
            save_clans(db, clan)  # Pass the db session to save_clans()

        print(f"✅ Successfully seeded database with {len(seed_clans)} clans.")

    except Exception as e:
        print(f"❌ Error while seeding the database: {str(e)}")

    finally:
        db.close()  # Ensure the db session is closed after seeding
