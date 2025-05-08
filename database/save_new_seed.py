import json
import os
from datetime import datetime
from database.database import load_clans, SessionLocal
from utils.logging import setup_logger
from utils.config import SEED_DIR

# Set up the logger
logger = setup_logger(__name__)

def generate_seed_file_path():
    """
    Generates the seed file path with today's date.
    """
    today_str = datetime.now().strftime("%Y%m%d")
    filename = f"clan_seed_{today_str}.json"
    return os.path.join(SEED_DIR, filename)

def export_clans_to_seed_file():
    """
    Exports all current clans from the database into a JSON seed file with today's date.
    """
    db = SessionLocal()
    seed_file_path = generate_seed_file_path()

    try:
        clans = load_clans(db)

        if not clans:
            logger.warning("No clans found in the database to export.")
            return None

        # Prepare data in a serializable format
        seed_data = [
            {
                "clan_id": clan.id,
                "clan_tag": clan.clan_tag,
                "clan_name": clan.clan_name,
                "country": str(clan.country)
            }
            for clan in clans
        ]

        # Write to JSON file
        os.makedirs(os.path.dirname(seed_file_path), exist_ok=True)
        with open(seed_file_path, 'w', encoding='utf-8') as f:
            json.dump(seed_data, f, ensure_ascii=False, indent=4)

        logger.info(f"✅ Successfully saved {len(seed_data)} clans to seed file: {seed_file_path}")
        return seed_file_path

    except Exception as e:
        logger.error(f"❌ Failed to export clans to seed file: {str(e)}")
        raise e

    finally:
        db.close()

if __name__ == "__main__":
    export_clans_to_seed_file()