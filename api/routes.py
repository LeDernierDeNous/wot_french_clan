import os
from fastapi import APIRouter, HTTPException, Depends
from importer_exporter.importer import update_clan_data
from importer_exporter.exporter import export_clans_to_csv, export_clans_to_txt
from scraper.scraper import get_languages
from utils.config import CSV_EXPORT_PATH, TXT_EXPORT_PATH
from api.model import Clan, Country
from api.crud import read_clan, get_clans_by_country, get_all_clans
from database.database import get_db
from sqlalchemy.orm import Session
from typing import List
from utils.logging import setup_logger

# Set up the logger for this file/module
logger = setup_logger(__name__)

router = APIRouter()

@router.get("/clans", response_model=List[Clan], summary="Get all clans", tags=["Clans"])
def get_all_clans_endpoint(db: Session = Depends(get_db)):
    """
    Returns all clans stored in the database.
    """
    try:
        clans = get_all_clans(db)
        logger.info(f"Successfully fetched {len(clans)} clans from the database.")
        return clans
    except Exception as e:
        logger.error(f"Error fetching all clans: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clans/{clan_id}", response_model=Clan, summary="Get a specific clan by clan_id", tags=["Clans"])
def get_clan(clan_id: int, db: Session = Depends(get_db)):
    """
    Returns details for a specific clan.
    """
    try:
        clan = read_clan(db, clan_id)
        if clan:
            logger.info(f"Successfully retrieved clan with ID {clan_id}.")
            return clan
        else:
            logger.warning(f"Clan with ID {clan_id} not found.")
            raise HTTPException(status_code=404, detail="Clan not found")
    except Exception as e:
        logger.error(f"Error fetching clan with ID {clan_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clans/update", summary="Update clan data", tags=["Clans"])
def update_clans():
    """
    Trigger an update of clan data using importer logic.
    """
    try:
        update_clan_data()
        logger.info("Clan data updated successfully.")
        return {"message": "Clan data updated successfully."}
    except Exception as e:
        logger.error(f"Error updating clan data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clans/export/csv", summary="Export clans data to CSV", tags=["Export"])
def export_csv():
    """
    Export the clan data to a CSV file.
    """
    try:
        export_clans_to_csv(CSV_EXPORT_PATH)
        logger.info(f"Exported clans to CSV: {CSV_EXPORT_PATH}")
        return {"message": f"Exported clans to CSV: {CSV_EXPORT_PATH}"}
    except Exception as e:
        logger.error(f"Error exporting clans to CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clans/export/txt", summary="Export clans data to TXT", tags=["Export"])
def export_txt():
    """
    Export the clan data to a TXT file.
    """
    try:
        export_clans_to_txt(TXT_EXPORT_PATH)
        logger.info(f"Exported clans to TXT: {TXT_EXPORT_PATH}")
        return {"message": f"Exported clans to TXT: {TXT_EXPORT_PATH}"}
    except Exception as e:
        logger.error(f"Error exporting clans to TXT: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clans/{clan_id}/languages", summary="Get languages for a clan", tags=["Scrapper"])
async def get_clan_languages(clan_id: int):
    """
    Uses web scraping to obtain a list of languages for a given clan.
    """
    try:
        languages = await get_languages(clan_id)
        logger.info(f"Successfully retrieved languages for clan ID {clan_id}.")
        return {"clan_id": clan_id, "languages": languages}
    except Exception as e:
        logger.error(f"Error retrieving languages for clan ID {clan_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/clans/country/{country_name}", response_model=list[Clan], summary="Get clans by country", tags=["Clans"])
def get_clans_by_country_endpoint(country_name: str, db: Session = Depends(get_db)):
    """
    Get all clans from a specific country.
    """
    try:
        clans = get_clans_by_country(db, country_name)
        logger.info(f"Successfully retrieved clans for country: {country_name}.")
        return clans
    except Exception as e:
        logger.error(f"Error retrieving clans for country {country_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/countries", response_model=List[str], summary="Get all countries", tags=["Countries"])
def get_all_countries():
    """
    Returns a list of all available countries.
    """
    try:
        countries = [country.name for country in Country]  # Adjust this line based on how Country is defined
        logger.info(f"Successfully retrieved all countries.")
        return countries
    except Exception as e:
        logger.error(f"Error retrieving countries: {e}")
        raise HTTPException(status_code=500, detail=str(e))
