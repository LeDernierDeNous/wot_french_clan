import json
from utils.config import FULL_JSON_PATH, FRENCH_JSON_PATH, SEED_DATA_PATH
from utils.logging import setup_logger

# Set up the logger for this file/module
logger = setup_logger(__name__)

def generate_seed(full_json_path, french_json_path, output_path):
    logger.info(f"Starting seed generation process.")
    
    # Load full clan dump
    try:
        with open(full_json_path, 'r', encoding='utf-8') as f:
            full_clans = json.load(f)
        logger.info(f"Successfully loaded full clan data from {full_json_path}.")
    except Exception as e:
        logger.error(f"Error loading full clan data from {full_json_path}: {e}")
        return

    # Load manually validated French clans
    try:
        with open(french_json_path, 'r', encoding='utf-8') as f:
            french_clans = json.load(f)
        logger.info(f"Successfully loaded French clan data from {french_json_path}.")
    except Exception as e:
        logger.error(f"Error loading French clan data from {french_json_path}: {e}")
        return

    seed_clans = []

    # Loop over all clans in the full data
    logger.info(f"Processing {len(full_clans)} clans from full data.")
    for clan_id, clan_info in full_clans.items():
        seed_clans.append({
            "clan_id": int(clan_id),
            "clan_tag": clan_info["clan_tag"],
            "clan_name": clan_info["clan_name"],
            "country": "UNKNOWN"  # Default country is "UNKNOWN"
        })

    # Loop over validated French clans
    logger.info(f"Processing {len(french_clans)} validated French clans.")
    for clan_id in french_clans:
        if clan_id in full_clans:
            clan_info = full_clans[clan_id]
            # Update country to "FRANCE" for validated French clans
            for seed_clan in seed_clans:
                if seed_clan["clan_id"] == int(clan_id):
                    seed_clan["country"] = "FRANCE"
                    break
            logger.info(f"Updated country for clan ID {clan_id} to FRANCE.")
        else:
            logger.warning(f"Clan ID {clan_id} not found in full data!")

    # Save final seed file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(seed_clans, f, ensure_ascii=False, indent=4)
        logger.info(f"Seed file generated successfully at {output_path} with {len(seed_clans)} clans.")
    except Exception as e:
        logger.error(f"Error saving seed file to {output_path}: {e}")
        return

if __name__ == "__main__":
    generate_seed(FULL_JSON_PATH, FRENCH_JSON_PATH, SEED_DATA_PATH)