# api/config.py

WG_API_KEY = "6267be451d158341277b1a61f3e32e97"
BASE_URL = (
    f"https://api.worldoftanks.eu/wgn/clans/list/?application_id={WG_API_KEY}"
    "&fields=clan_id%2Cname%2Ctag&game=wot&language=fr&search="
)

CSV_EXPORT_PATH = "data/export/clans.csv"
TXT_EXPORT_PATH = "data/export/clans.txt"

DATABASE_URL = "sqlite:///data/database/clans.db"

FULL_JSON_PATH = 'data/raw/Full_version_french_clan_list.json'
FRENCH_JSON_PATH = 'data/raw/Safe_version_french_clan_list.json'
SEED_DATA_PATH = 'data/seed/seed_data.json'