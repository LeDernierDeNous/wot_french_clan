import json
from database.database import save_clans  # Your database system expects a dict
import os
from api.config import SEED_DATA_PATH

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
    try:
        seed_clans = load_seed_data(SEED_DATA_PATH)
        
        # Transform into a dict where keys are clan_id (str) for saving
        clans_dict = {
            str(clan['clan_id']): {
                "clan_tag": clan['clan_tag'],
                "clan_name": clan['clan_name'],
                "country": clan.get('country', "Unknown")
            }
            for clan in seed_clans
        }

        save_clans(clans_dict)
        print(f"✅ Successfully seeded database with {len(clans_dict)} clans.")

    except Exception as e:
        print(f"❌ Error while seeding the database: {str(e)}")

if __name__ == "__main__":
    seed_database()
