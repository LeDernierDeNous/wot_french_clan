import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

WG_API_KEY = os.getenv("WG_API_KEY")
if WG_API_KEY is None:
    raise ValueError("WG_API_KEY not found in .env file")

# f"https://api.worldoftanks.eu/wgn/clans/list/?application_id={WG_API_KEY}&fields=clan_id%2Cname%2Ctag&game=wot&language=fr&search="

BASE_URL = (
    f"https://api.worldoftanks.eu/wgn/clans/info/?application_id={WG_API_KEY}&game=wot&language=fr&fields=clan_id%2Cname%2Ctag&clan_id="
)

CSV_EXPORT_PATH = "data/export/clans.csv"
TXT_EXPORT_PATH = "data/export/clans.txt"

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
DATABASE_URL = "sqlite:///./data/database/clans.db"

FULL_JSON_PATH = 'data/raw/Full_version_french_clan_list.json'
FRENCH_JSON_PATH = 'data/raw/Safe_version_french_clan_list.json'
SEED_DIR = "data/seed"
SEED_DATA_PATH = f'{SEED_DIR}/seed_data.json'