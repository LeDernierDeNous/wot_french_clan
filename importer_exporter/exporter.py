import csv
import os
from database.database import load_clans

def export_clans_to_csv(filepath: str):
    """
    Export clan data to a CSV file.
    """
    clans = load_clans()

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Clan Tag", "Clan Name"])
        for clan_id, data in clans.items():
            writer.writerow([clan_id, data.get("clan_tag"), data.get("clan_name")])

def export_clans_to_txt(filepath: str):
    """
    Export clan data to a TXT file.
    """
    clans = load_clans()

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as txtfile:
        for clan_id, data in clans.items():
            txtfile.write(f"ID: {clan_id}\n")
            txtfile.write(f"Clan Tag: {data.get('clan_tag')}\n")
            txtfile.write(f"Clan Name: {data.get('clan_name')}\n\n")
