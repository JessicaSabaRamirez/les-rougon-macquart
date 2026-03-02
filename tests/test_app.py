"""
Test suite for Les Rougon-Macquart companion app.
Run with: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Use in-memory SQLite for tests
TEST_DB = "sqlite:///./test_rm.db"

os.environ["DB_PATH"] = "./test_rm.db"

from app.models import Base
from app.database import get_db
from app.main import app

# Test engine
engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create tables and seed test data once per test session."""
    Base.metadata.create_all(bind=engine)
    # Run seed with test DB
    from data.seed import run
    run()
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    import app.database as _db
    _db.engine.dispose()
    if os.path.exists("./test_rm.db"):
        os.remove("./test_rm.db")


@pytest.fixture
def client():
    return TestClient(app)


# ── Data integrity tests ─────────────────────────────────────────────────────

class TestDataIntegrity:

    def test_all_20_novels_present(self):
        db = TestingSessionLocal()
        from app.models import Novel
        count = db.query(Novel).count()
        db.close()
        assert count == 20, f"Expected 20 novels, found {count}"

    def test_novels_numbered_1_to_20(self):
        db = TestingSessionLocal()
        from app.models import Novel
        numbers = {n.number for n in db.query(Novel).all()}
        db.close()
        assert numbers == set(range(1, 21))

    def test_no_novel_missing_title(self):
        db = TestingSessionLocal()
        from app.models import Novel
        bad = db.query(Novel).filter(
            (Novel.title_fr == None) | (Novel.title_en == None)
        ).all()
        db.close()
        assert len(bad) == 0

    def test_no_character_missing_name(self):
        db = TestingSessionLocal()
        from app.models import Character
        bad = db.query(Character).filter(Character.name == None).all()
        db.close()
        assert len(bad) == 0

    def test_no_duplicate_character_slugs(self):
        db = TestingSessionLocal()
        from app.models import Character
        from sqlalchemy import func
        dupes = (
            db.query(Character.slug, func.count(Character.slug).label("n"))
            .group_by(Character.slug)
            .having(func.count(Character.slug) > 1)
            .all()
        )
        db.close()
        assert len(dupes) == 0, f"Duplicate slugs found: {dupes}"

    def test_no_duplicate_novel_slugs(self):
        db = TestingSessionLocal()
        from app.models import Novel
        from sqlalchemy import func
        dupes = (
            db.query(Novel.slug, func.count(Novel.slug).label("n"))
            .group_by(Novel.slug)
            .having(func.count(Novel.slug) > 1)
            .all()
        )
        db.close()
        assert len(dupes) == 0

    def test_all_relations_reference_valid_characters(self):
        db = TestingSessionLocal()
        from app.models import CharacterRelation, Character
        char_ids = {c.id for c in db.query(Character).all()}
        rels = db.query(CharacterRelation).all()
        db.close()
        for rel in rels:
            assert rel.character_a_id in char_ids, f"Invalid character_a_id {rel.character_a_id}"
            assert rel.character_b_id in char_ids, f"Invalid character_b_id {rel.character_b_id}"

    def test_major_characters_have_descriptions(self):
        db = TestingSessionLocal()
        from app.models import Character
        no_desc = db.query(Character).filter(
            Character.featured_on_landing == True,
            Character.description_en == None
        ).all()
        db.close()
        assert len(no_desc) == 0, f"Featured characters missing descriptions: {[c.name for c in no_desc]}"

    def test_at_least_50_characters(self):
        db = TestingSessionLocal()
        from app.models import Character
        count = db.query(Character).count()
        db.close()
        assert count >= 50, f"Expected at least 50 characters, found {count}"

    def test_key_locations_present(self):
        db = TestingSessionLocal()
        from app.models import Location
        slugs = {l.slug for l in db.query(Location).all()}
        db.close()
        for expected in ["paris", "plassans", "montsou"]:
            assert expected in slugs, f"Expected location '{expected}' not found"


# ── API / routing tests ──────────────────────────────────────────────────────

class TestRoutes:

    def test_homepage_200(self, client):
        r = client.get("/")
        assert r.status_code == 200

    def test_health_endpoint(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}

    def test_characters_list_200(self, client):
        r = client.get("/characters")
        assert r.status_code == 200

    def test_character_detail_valid_slug(self, client):
        r = client.get("/characters/gervaise-macquart")
        assert r.status_code == 200
        assert "Gervaise" in r.text

    def test_character_detail_invalid_slug_404(self, client):
        r = client.get("/characters/nobody-here-xxxx")
        assert r.status_code == 404

    def test_novels_list_200(self, client):
        r = client.get("/novels")
        assert r.status_code == 200

    def test_novel_detail_valid_slug(self, client):
        r = client.get("/novels/germinal")
        assert r.status_code == 200
        assert "Germinal" in r.text

    def test_novel_detail_invalid_slug_404(self, client):
        r = client.get("/novels/not-a-novel")
        assert r.status_code == 404

    def test_locations_list_200(self, client):
        r = client.get("/locations")
        assert r.status_code == 200

    def test_location_detail_valid_slug(self, client):
        r = client.get("/locations/paris")
        assert r.status_code == 200
        assert "Paris" in r.text

    def test_search_page_200(self, client):
        r = client.get("/search")
        assert r.status_code == 200

    def test_search_with_query(self, client):
        r = client.get("/search?q=gervaise")
        assert r.status_code == 200
        assert "Gervaise" in r.text

    def test_landing_tree_api(self, client):
        r = client.get("/characters/api/landing-tree")
        assert r.status_code == 200
        data = r.json()
        assert "characters" in data
        assert "relations" in data
        assert len(data["characters"]) > 0


# ── Search tests ─────────────────────────────────────────────────────────────

class TestSearch:

    def test_search_api_returns_results_for_known_character(self, client):
        for name in ["Gervaise", "Nana", "Lantier", "Saccard"]:
            r = client.get(f"/search/api?q={name}")
            assert r.status_code == 200
            data = r.json()
            assert len(data["results"]) > 0, f"No results for '{name}'"

    def test_search_api_empty_query(self, client):
        r = client.get("/search/api?q=")
        assert r.status_code == 200
        assert r.json() == {"results": []}

    def test_search_api_short_query(self, client):
        r = client.get("/search/api?q=a")
        assert r.status_code == 200
        assert r.json() == {"results": []}

    def test_search_finds_germinal(self, client):
        r = client.get("/search/api?q=Germinal")
        assert r.status_code == 200
        results = r.json()["results"]
        names = [res["name"] for res in results]
        assert any("Germinal" in n for n in names)


# ── Timeline tests ────────────────────────────────────────────────────────────

class TestTimeline:

    def test_timeline_page_200(self, client):
        r = client.get("/timeline")
        assert r.status_code == 200

    def test_timeline_contains_events(self, client):
        r = client.get("/timeline")
        assert "1851" in r.text
        assert "1871" in r.text

    def test_at_least_15_events_seeded(self):
        db = TestingSessionLocal()
        from app.models import Event
        count = db.query(Event).count()
        db.close()
        assert count >= 15, f"Expected at least 15 events, found {count}"

    def test_events_have_types(self):
        db = TestingSessionLocal()
        from app.models import Event
        types = {e.event_type for e in db.query(Event).all()}
        db.close()
        assert "historical" in types
        assert "personal" in types

    def test_events_have_years(self):
        db = TestingSessionLocal()
        from app.models import Event
        no_year = db.query(Event).filter(Event.year == None).all()
        db.close()
        assert len(no_year) == 0, "Some events are missing a year"


# ── Quotes tests ──────────────────────────────────────────────────────────────

class TestQuotes:

    def test_quotes_page_200(self, client):
        r = client.get("/quotes")
        assert r.status_code == 200

    def test_quotes_page_contains_text(self, client):
        r = client.get("/quotes")
        assert "germinal" in r.text.lower() or "Germinal" in r.text

    def test_at_least_10_quotes_seeded(self):
        db = TestingSessionLocal()
        from app.models import Quote
        count = db.query(Quote).count()
        db.close()
        assert count >= 10, f"Expected at least 10 quotes, found {count}"

    def test_quotes_have_french_text(self):
        db = TestingSessionLocal()
        from app.models import Quote
        no_fr = db.query(Quote).filter(Quote.text_fr == None).all()
        db.close()
        assert len(no_fr) == 0, "Some quotes are missing French text"

    def test_quotes_novel_filter(self, client):
        r = client.get("/quotes?novel=germinal")
        assert r.status_code == 200
        assert "germinal" in r.text.lower() or "Germinal" in r.text

    def test_quotes_invalid_novel_filter(self, client):
        r = client.get("/quotes?novel=not-a-novel")
        assert r.status_code == 200
