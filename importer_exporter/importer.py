from database.database import load_clans, save_clans
import requests

# You can later make these constants configurable
APPLICATION_ID = "6267be451d158341277b1a61f3e32e97"
BASE_API_URL = f"https://api.worldoftanks.eu/wgn/clans/list/?application_id={APPLICATION_ID}&fields=clan_id%2Cname%2Ctag&game=wot&language=fr&search="

def update_clan_data():
    """
    Dummy function to simulate a clan update.
    Ideally you would provide a list of clan tags or some other mechanism.
    """
    # For now, just reload and save again (you can later improve this).
    clans = load_clans()

    # Example: Adding a static fake clan
    new_clan_id = 999999
    clans[str(new_clan_id)] = {
        "clan_tag": "FAKE",
        "clan_name": "Fake Clan Name"
    }

    save_clans(clans)
