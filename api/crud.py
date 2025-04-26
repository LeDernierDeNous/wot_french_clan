from sqlalchemy.orm import Session
from models import Clan, Country
from sqlalchemy.exc import IntegrityError

def create_clan(db: Session, clan_id: int, clan_tag: str, clan_name: str, country: str):
    """
    Create a new clan entry in the database.
    """
    # Convert the country to an Enum (validating it is an actual country)
    try:
        country_enum = Country[country.upper()]
    except KeyError:
        raise ValueError(f"Invalid country: {country}")

    new_clan = Clan(
        id=clan_id,
        clan_tag=clan_tag,
        clan_name=clan_name,
        country=country_enum
    )

    try:
        db.add(new_clan)
        db.commit()
        db.refresh(new_clan)
        return new_clan
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
    return db.query(Clan).filter(Clan.id == clan_id).first()


def update_clan(db: Session, clan_id: int, clan_tag: str = None, clan_name: str = None, country: str = None):
    """
    Update an existing clan's tag, name, or country.
    """
    clan = db.query(Clan).filter(Clan.id == clan_id).first()
    
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
    return clan


def delete_clan(db: Session, clan_id: int):
    """
    Delete a clan entry by its ID.
    """
    clan = db.query(Clan).filter(Clan.id == clan_id).first()

    if not clan:
        raise ValueError(f"Clan with ID {clan_id} does not exist.")
    
    db.delete(clan)
    db.commit()
    return {"message": f"Clan with ID {clan_id} has been deleted."}
