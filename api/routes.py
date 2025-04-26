# routes.py

import os
from fastapi import APIRouter, HTTPException
from importer_exporter.importer import update_clan_data
from importer_exporter.exporter import export_clans_to_csv, export_clans_to_txt
from database.database import load_clans  # load_clans() returns a dict of clans
from scraper.scraping import get_languages
from wot_french_clan_api.config import CSV_EXPORT_PATH, TXT_EXPORT_PATH

router = APIRouter()

@router.get("/clans", summary="Get all clans")
def get_all_clans():
    """
    Returns all clans stored in the database.
    """
    try:
        clans = load_clans()
        return clans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clans/{clan_id}", summary="Get a specific clan by clan_id")
def get_clan(clan_id: str):
    """
    Returns details for a specific clan.
    """
    try:
        clans = load_clans()
        if clan_id in clans:
            return clans[clan_id]
        else:
            raise HTTPException(status_code=404, detail="Clan not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clans/update", summary="Update clan data")
def update_clans():
    """
    Trigger an update of clan data using importer logic.
    """
    try:
        update_clan_data()
        return {"message": "Clan data updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clans/export/csv", summary="Export clans data to CSV")
def export_csv():
    """
    Export the clan data to a CSV file.
    """
    try:
        export_clans_to_csv(CSV_EXPORT_PATH)
        return {"message": f"Exported clans to CSV: {CSV_EXPORT_PATH}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clans/export/txt", summary="Export clans data to TXT")
def export_txt():
    """
    Export the clan data to a TXT file.
    """
    try:
        export_clans_to_txt(TXT_EXPORT_PATH)
        return {"message": f"Exported clans to TXT: {TXT_EXPORT_PATH}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clans/{clan_id}/languages", summary="Get languages for a clan")
async def get_clan_languages(clan_id: str):
    """
    Uses web scraping to obtain a list of languages for a given clan.
    Note: clan_id should be convertible to int.
    """
    try:
        # Convert clan_id to integer as required by the scraper function.
        languages = await get_languages(int(clan_id))
        return {"clan_id": clan_id, "languages": languages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
