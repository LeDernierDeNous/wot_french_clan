# api/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from enum import Enum

# Create a Base class for SQLAlchemy models
Base = declarative_base()
class Country(str, Enum):
    ALBANIA = "Albania"
    ANDORRA = "Andorra"
    AUSTRIA = "Austria"
    BELARUS = "Belarus"
    BELGIUM = "Belgium"
    BOSNIA_AND_HERZEGOVINA = "Bosnia and Herzegovina"
    BULGARIA = "Bulgaria"
    CROATIA = "Croatia"
    CYPRUS = "Cyprus"
    CZECH_REPUBLIC = "Czech Republic"
    DENMARK = "Denmark"
    ESTONIA = "Estonia"
    FINLAND = "Finland"
    FRANCE = "France"
    GERMANY = "Germany"
    GREECE = "Greece"
    HUNGARY = "Hungary"
    ICELAND = "Iceland"
    IRELAND = "Ireland"
    ITALY = "Italy"
    KOSOVO = "Kosovo"
    LATVIA = "Latvia"
    LIECHTENSTEIN = "Liechtenstein"
    LITHUANIA = "Lithuania"
    LUXEMBOURG = "Luxembourg"
    MALTA = "Malta"
    MOLDOVA = "Moldova"
    MONACO = "Monaco"
    MONTENEGRO = "Montenegro"
    NETHERLANDS = "Netherlands"
    NORTH_MACEDONIA = "North Macedonia"
    NORWAY = "Norway"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    ROMANIA = "Romania"
    SAN_MARINO = "San Marino"
    SERBIA = "Serbia"
    SLOVAKIA = "Slovakia"
    SLOVENIA = "Slovenia"
    SPAIN = "Spain"
    SWEDEN = "Sweden"
    SWITZERLAND = "Switzerland"
    UKRAINE = "Ukraine"
    UNITED_KINGDOM = "United Kingdom"
    VATICAN_CITY = "Vatican City"
    INTERNATIONAL = "International"  # Special case
    UNKNOWN = "Unknown"
class ClanSQL(Base):
    __tablename__ = 'clans'

    id: int = Column(Integer, primary_key=True, index=True)
    clan_tag: str = Column(String, unique=True, index=True)
    clan_name: str = Column(String)
    country: Country = Column(String, default=Country.UNKNOWN)

    def __repr__(self):
        return f"<ClanSQL(id={self.id}, clan_tag={self.clan_tag}, clan_name={self.clan_name}, country={self.country})>"

# Pydantic base model for Clan
class Clan(BaseModel):
    id: int
    clan_tag: str
    clan_name: str
    country: Country
    class Config:
        from_attributes = True