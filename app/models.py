"""
SQLAlchemy models for Les Rougon-Macquart companion app.
All tables use SQLite via SQLAlchemy Core / ORM.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    ForeignKey, Table, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ── Many-to-many: character ↔ novel appearances ────────────────────────────
class CharacterAppearance(Base):
    __tablename__ = "character_appearances"
    id             = Column(Integer, primary_key=True)
    character_id   = Column(Integer, ForeignKey("characters.id"), nullable=False)
    novel_id       = Column(Integer, ForeignKey("novels.id"), nullable=False)
    role           = Column(String(20), default="major")   # major | minor | mentioned
    spoiler_level  = Column(Integer, default=0)            # 0 = safe, 1 = mild, 2 = heavy
    __table_args__ = (UniqueConstraint("character_id", "novel_id"),)


# ── Many-to-many: event ↔ character ───────────────────────────────────────
class EventCharacter(Base):
    __tablename__ = "event_characters"
    id           = Column(Integer, primary_key=True)
    event_id     = Column(Integer, ForeignKey("events.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)


# ── Core tables ────────────────────────────────────────────────────────────

class Novel(Base):
    __tablename__ = "novels"

    id           = Column(Integer, primary_key=True)
    number       = Column(Integer, nullable=False)          # 1–20 in series order
    slug         = Column(String(80), unique=True, nullable=False)
    title_fr     = Column(String(120), nullable=False)
    title_en     = Column(String(120), nullable=False)
    year         = Column(Integer)
    summary_en   = Column(Text)
    summary_fr   = Column(Text)
    themes       = Column(Text)                             # comma-separated
    setting      = Column(String(120))                      # primary location

    appearances  = relationship("CharacterAppearance", backref="novel", cascade="all, delete-orphan")
    events       = relationship("Event", backref="novel")

    def to_dict(self):
        return {
            "id": self.id, "number": self.number, "slug": self.slug,
            "title_fr": self.title_fr, "title_en": self.title_en,
            "year": self.year, "summary_en": self.summary_en,
            "summary_fr": self.summary_fr, "themes": self.themes,
            "setting": self.setting,
        }


class Character(Base):
    __tablename__ = "characters"

    id                  = Column(Integer, primary_key=True)
    slug                = Column(String(80), unique=True, nullable=False)
    name                = Column(String(120), nullable=False)
    birth_name          = Column(String(120))               # if different
    occupation          = Column(String(120))
    branch              = Column(String(20))                # rougon | macquart | mouret | other
    generation          = Column(Integer)                   # 0=founders, 1,2,3...
    description_en      = Column(Text)
    description_fr      = Column(Text)
    physical_en         = Column(Text)
    physical_fr         = Column(Text)
    image_url           = Column(String(255))               # Wikimedia or local
    image_credit        = Column(String(255))
    # Family tree positioning hint (for the SVG layout engine)
    tree_x              = Column(Float)
    tree_y              = Column(Float)
    featured_on_landing = Column(Boolean, default=False)    # shown on landing page tree

    appearances  = relationship("CharacterAppearance", backref="character", cascade="all, delete-orphan")
    quotes       = relationship("Quote", backref="character")
    events       = relationship("EventCharacter", backref="character")

    # Relations where this character is the subject
    relations_as_a = relationship("CharacterRelation",
                                  foreign_keys="CharacterRelation.character_a_id",
                                  backref="character_a", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id, "slug": self.slug, "name": self.name,
            "birth_name": self.birth_name, "occupation": self.occupation,
            "branch": self.branch, "generation": self.generation,
            "description_en": self.description_en, "description_fr": self.description_fr,
            "physical_en": self.physical_en, "physical_fr": self.physical_fr,
            "image_url": self.image_url, "image_credit": self.image_credit,
            "featured_on_landing": self.featured_on_landing,
        }


class CharacterRelation(Base):
    __tablename__ = "character_relations"

    id             = Column(Integer, primary_key=True)
    character_a_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    character_b_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    relation_type  = Column(String(40), nullable=False)
    # e.g. parent | child | sibling | spouse | lover | employer | friend | enemy
    description    = Column(Text)
    __table_args__ = (UniqueConstraint("character_a_id", "character_b_id", "relation_type"),)


class Location(Base):
    __tablename__ = "locations"

    id             = Column(Integer, primary_key=True)
    slug           = Column(String(80), unique=True, nullable=False)
    name           = Column(String(120), nullable=False)
    location_type  = Column(String(40))   # city | district | building | mine | estate | region
    description_en = Column(Text)
    description_fr = Column(Text)
    image_url      = Column(String(255))
    latitude       = Column(Float)
    longitude      = Column(Float)
    featured       = Column(Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id, "slug": self.slug, "name": self.name,
            "location_type": self.location_type,
            "description_en": self.description_en,
            "description_fr": self.description_fr,
            "image_url": self.image_url,
            "latitude": self.latitude, "longitude": self.longitude,
        }


class Event(Base):
    __tablename__ = "events"

    id           = Column(Integer, primary_key=True)
    title_en     = Column(String(200), nullable=False)
    title_fr     = Column(String(200))
    year         = Column(Integer)
    date_approx  = Column(String(40))   # e.g. "Winter 1869"
    description_en = Column(Text)
    description_fr = Column(Text)
    novel_id     = Column(Integer, ForeignKey("novels.id"))
    event_type   = Column(String(40))   # historical | personal | political

    characters   = relationship("EventCharacter", backref="event")


class Quote(Base):
    __tablename__ = "quotes"

    id          = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    novel_id    = Column(Integer, ForeignKey("novels.id"))
    text_fr     = Column(Text, nullable=False)
    text_en     = Column(Text)
    context     = Column(Text)
    page_ref    = Column(String(40))

    novel       = relationship("Novel")
