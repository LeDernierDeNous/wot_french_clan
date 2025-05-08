import json
import os
from fastapi import APIRouter, HTTPException, Depends
import requests
from importer_exporter.importer import update_clan_data
from importer_exporter.exporter import export_clans_to_csv, export_clans_to_txt
from scraper.scraper import get_languages
from utils.config import CSV_EXPORT_PATH, TXT_EXPORT_PATH
from api.model import Clan, Country, ClanInsertRequest
from api.crud import read_clan, get_clans_by_country, get_all_clans, create_clan
from database.database import get_db
from sqlalchemy.orm import Session
from typing import List
from utils.logging import setup_logger
from utils.config import WG_API_KEY, BASE_URL
from database.save_new_seed import export_clans_to_seed_file

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

@router.post("/clans/insert_by_id", response_model=Clan, summary="Insert a new clan by ID", tags=["Clans"])
def insert_new_clan_by_id(clan_data: ClanInsertRequest, db: Session = Depends(get_db)):
    """
    Inserts a new clan into the database by fetching name and tag from the Wargaming API.
    """
    try:
        # Validate and convert country
        response = requests.get(f"{BASE_URL}{clan_data.id}")
        response.raise_for_status()
        wg_result = response.json()

        logger.debug(f"WG API response: {json.dumps(wg_result, indent=2)}")

        # Check if the clan ID exists in the response
        wg_clan = wg_result.get("data", {}).get(str(clan_data.id))
        if not wg_clan:
            logger.warning(f"Clan ID {clan_data.id} not found in WG API.")
            raise HTTPException(status_code=404, detail="Clan not found in WG API")

        # Use Pydantic model to normalize/validate country
        try:
            clan_model = Clan(
                id=clan_data.id,
                clan_tag=wg_clan["tag"],
                clan_name=wg_clan["name"],
                country=clan_data.country
            )
        except ValueError as ve:
            logger.warning(f"Validation error: {ve}")
            raise ve

        # Call DB creation
        try:
            return create_clan(
                db=db,
                clan_id=clan_model.id,
                clan_tag=clan_model.clan_tag,
                clan_name=clan_model.clan_name,
                country=clan_model.country.value  # .value needed for Enum to str
            )
        except ValueError as ve:
            logger.warning(f"Database error: {ve}")
            raise ve

    except HTTPException:
        raise  # Let FastAPI handle any HTTPExceptions you raise explicitly
    except ValueError as ve:
        logger.warning(f"Validation error inserting clan: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except requests.HTTPError as http_err:
        logger.error(f"WG API error: {http_err}")
        raise HTTPException(status_code=502, detail="Failed to fetch clan from WG API")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

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

@router.post("/clans/insert", response_model=Clan, summary="Insert a new clan", tags=["Clans"])
def insert_new_clan(clan_data: Clan, db: Session = Depends(get_db)):
    """
    Inserts a new clan into the database.
    """
    try:
        clan = create_clan(
            db=db,
            clan_id=clan_data.id,
            clan_tag=clan_data.clan_tag,
            clan_name=clan_data.clan_name,
            country=clan_data.country,
        )
        logger.info(f"Successfully inserted clan with ID {clan_data.id}.")
        return clan
    except ValueError as ve:
        logger.warning(f"Validation error inserting clan: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error inserting clan: {e}")
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

@router.post("/clans/save_seed", summary="Export clans to a seed file", tags=["Utilities"])
def save_seed_file():
    """
    Exports all current clans to a seed file with today's date.
    """
    try:
        path = export_clans_to_seed_file()
        if path:
            return {"message": "✅ Seed file saved", "path": path}
        else:
            raise HTTPException(status_code=404, detail="No clans to export.")
    except Exception as e:
        logger.error(f"Error exporting seed: {e}")
        raise HTTPException(status_code=500, detail="Failed to export seed file")