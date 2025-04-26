from typing import List
from sqlalchemy.orm import Session
from api.model import ClanSQL, Country, Clan
from sqlalchemy.exc import IntegrityError

def create_clan(db: Session, clan_id: int, clan_tag: str, clan_name: str, country: str):
    """
    Create a new clan entry in the database.
    """
    # Validate and convert country
    try:
        country_enum = Country[country.upper()]
    except KeyError:
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
        return Clan.model_validate(new_clan)  # Use model_validate instead of from_orm
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Clan with ID {clan_id} already exists.")
    except Exception as e:
        db.rollback()
        raise ValueError(f"An error occurred while creating the clan: {e}")

def read_clan(db: Session, clan_id: int):
    """
    Read a clan's information by its ID.
    """
    clan = db.query(ClanSQL).filter(ClanSQL.id == clan_id).first()  # Use ClanSQL for database query
    if clan:
        return Clan.model_validate(clan)  # Use model_validate instead of from_orm
    return None

def update_clan(db: Session, clan_id: int, clan_tag: str = None, clan_name: str = None, country: str = None):
    """
    Update an existing clan's tag, name, or country.
    """
    clan = db.query(ClanSQL).filter(ClanSQL.id == clan_id).first()  # Use ClanSQL for database query
    
    if not clan:
        raise ValueError(f"Clan with ID {clan_id} does not exist.")
    
    if clan_tag:
        clan.clan_tag = clan_tag
    if clan_name:
        clan.clan_name = clan_name
    if country:
        try:
            country_enum = Country[country.upper()]
            clan.country = country_enum
        except KeyError:
            raise ValueError(f"Invalid country: {country}")

    db.commit()
    db.refresh(clan)
    return Clan.model_validate(clan)  # Use model_validate instead of from_orm

def delete_clan(db: Session, clan_id: int):
    """
    Delete a clan entry by its ID.
    """
    clan = db.query(ClanSQL).filter(ClanSQL.id == clan_id).first()  # Use ClanSQL for database query

    if not clan:
        raise ValueError(f"Clan with ID {clan_id} does not exist.")
    
    db.delete(clan)
    db.commit()
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
        return db.query(ClanSQL).all()
    except Exception as e:
        logging.error(f"Error fetching clans: {e}")
        raise

def get_clans_by_country(db: Session, country: str):
    """
    Get all clans from a specific country.
    """
    # Normalize the input by replacing spaces with underscores
    country_normalized = country.replace(" ", "_").upper()
    
    try:
        # Match the country to the Enum (after normalization)
        country_enum = Country[country_normalized]
    except KeyError:
        raise ValueError(f"Invalid country: {country}")

    # Query using the SQLAlchemy model (ClanSQL)
    clans_db = db.query(ClanSQL).filter(ClanSQL.country == country_enum).all()

    # Convert the SQLAlchemy results to Pydantic models
    return [Clan.model_validate(clan) for clan in clans_db]