from typing import List
from sqlalchemy.orm import Session
from api.model import ClanSQL, Country, Clan
from sqlalchemy.exc import IntegrityError
from utils.logging import setup_logger

# Set up the logger for this file/module
logger = setup_logger(__name__)

def create_clan(db: Session, clan_id: int, clan_tag: str, clan_name: str, country: str):
    """
    Create a new clan entry in the database.
    """
    # Validate and convert country
    try:
        country_enum = Country[country.upper()]
    except KeyError:
        logger.error(f"Invalid country provided: {country}")
        raise ValueError(f"Invalid country: {country}")

    # Instantiate SQLAlchemy model (ClanSQL) instead of Pydantic model (Clan)
    new_clan = ClanSQL(
        id=clan_id,
        clan_tag=clan_tag,
        clan_name=clan_name,
        country=country_enum
    )

    try:
        db.add(new_clan)
        db.commit()
        db.refresh(new_clan)
        logger.info(f"Successfully created clan: {clan_name} with ID: {clan_id}")
        return Clan.model_validate(new_clan)  # Use model_validate instead of from_orm
    except IntegrityError:
        db.rollback()
        logger.error(f"Clan with ID {clan_id} already exists.")
        raise ValueError(f"Clan with ID {clan_id} already exists.")
    except Exception as e:
        db.rollback()
        logger.error(f"An error occurred while creating the clan: {e}")
        raise ValueError(f"An error occurred while creating the clan: {e}")

def read_clan(db: Session, clan_id: int):
    """
    Read a clan's information by its ID.
    """
    clan = db.query(ClanSQL).filter(ClanSQL.id == clan_id).first()  # Use ClanSQL for database query
    if clan:
        logger.info(f"Successfully retrieved clan: {clan_id}")
        return Clan.model_validate(clan)  # Use model_validate instead of from_orm
    else:
        logger.warning(f"Clan with ID {clan_id} not found.")
    return None

def update_clan(db: Session, clan_id: int, clan_tag: str = None, clan_name: str = None, country: str = None):
    """
    Update an existing clan's tag, name, or country.
    """
    clan = db.query(ClanSQL).filter(ClanSQL.id == clan_id).first()  # Use ClanSQL for database query
    
    if not clan:
        logger.warning(f"Clan with ID {clan_id} does not exist.")
        raise ValueError(f"Clan with ID {clan_id} does not exist.")
    
    if clan_tag:
        logger.info(f"Updating clan tag to {clan_tag} for clan ID {clan_id}")
        clan.clan_tag = clan_tag
    if clan_name:
        logger.info(f"Updating clan name to {clan_name} for clan ID {clan_id}")
        clan.clan_name = clan_name
    if country:
        try:
            country_enum = Country[country.upper()]
            logger.info(f"Updating country to {country_enum} for clan ID {clan_id}")
            clan.country = country_enum
        except KeyError:
            logger.error(f"Invalid country: {country} for clan ID {clan_id}")
            raise ValueError(f"Invalid country: {country}")

    db.commit()
    db.refresh(clan)
    logger.info(f"Successfully updated clan ID {clan_id}")
    return Clan.model_validate(clan)  # Use model_validate instead of from_orm

def delete_clan(db: Session, clan_id: int):
    """
    Delete a clan entry by its ID.
    """
    clan = db.query(ClanSQL).filter(ClanSQL.id == clan_id).first()  # Use ClanSQL for database query

    if not clan:
        logger.warning(f"Clan with ID {clan_id} does not exist.")
        raise ValueError(f"Clan with ID {clan_id} does not exist.")
    
    db.delete(clan)
    db.commit()
    logger.info(f"Successfully deleted clan ID {clan_id}")
    return {"message": f"Clan with ID {clan_id} has been deleted."}

def get_all_clans(db: Session) -> List[ClanSQL]:
    """
    Get all clans from the database.

    Args:
        db: Database session to query the database.

    Returns:
        A list of ClanSQL objects.
    """
    try:
        clans = db.query(ClanSQL).all()
        logger.info(f"Successfully retrieved {len(clans)} clans.")
        return clans
    except Exception as e:
        logger.error(f"Error fetching clans: {e}")
        raise

def get_clans_by_country(db: Session, country: str):
    """
    Get all clans from a specific country.
    """
    # Normalize the input by replacing spaces with underscores and uppercasing
    country_normalized = country.replace(" ", "_").upper()
    
    try:
        # Match the input to the Enum
        country_enum = Country[country_normalized]
        logger.info(f"Fetching clans for country: {country_enum.value}")
    except KeyError:
        logger.error(f"Invalid country: {country}")
        raise ValueError(f"Invalid country: {country}")

    try:
        # Query the database with the country value (in DB format: UPPER)
        clans_db = db.query(ClanSQL).filter(ClanSQL.country == country_enum.value.upper()).all()

        if clans_db:
            logger.info(f"Successfully retrieved {len(clans_db)} clans for country: {country_enum.value}")
        else:
            logger.info(f"No clans found for country: {country_enum.value}")

        # Before validating, fix the country value to match Pydantic expectations (title-case)
        clans_fixed = []
        for clan in clans_db:
            clan_dict = clan.__dict__.copy()
            clan_dict['country'] = clan.country.title()
            clans_fixed.append(Clan.model_validate(clan_dict))
        
        return clans_fixed

    except Exception as e:
        logger.error(f"Error while fetching clans for country {country_enum.value}: {str(e)}")
        raise