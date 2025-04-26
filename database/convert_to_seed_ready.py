import json
from api.config import FULL_JSON_PATH, FRENCH_JSON_PATH, SEED_DATA_PATH

def generate_seed(full_json_path, french_json_path, output_path):
    # Load full clan dump
    with open(full_json_path, 'r', encoding='utf-8') as f:
        full_clans = json.load(f)
    
    # Load manually validated French clans
    with open(french_json_path, 'r', encoding='utf-8') as f:
        french_clans = json.load(f)

    seed_clans = []

    # Loop over all clans in the full data
    for clan_id, clan_info in full_clans.items():
        seed_clans.append({
            "clan_id": int(clan_id),
            "clan_tag": clan_info["clan_tag"],
            "clan_name": clan_info["clan_name"],
            "country": "UNKNOWN"  # Default country is "UNKNOWN"
        })

    # Loop over validated French clans
    for clan_id in french_clans:
        if clan_id in full_clans:
            clan_info = full_clans[clan_id]
            # Update country to "FRANCE" for validated French clans
            for seed_clan in seed_clans:
                if seed_clan["clan_id"] == int(clan_id):
                    seed_clan["country"] = "FRANCE"
                    break
        else:
            print(f"Warning: Clan ID {clan_id} not found in full data!")

    # Save final seed file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(seed_clans, f, ensure_ascii=False, indent=4)

    print(f"✅ Seed file generated at {output_path} with {len(seed_clans)} clans.")

if __name__ == "__main__":
    generate_seed(FULL_JSON_PATH, FRENCH_JSON_PATH, SEED_DATA_PATH)
