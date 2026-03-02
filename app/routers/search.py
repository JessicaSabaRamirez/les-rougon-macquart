"""Search router — full-text search across characters, novels, locations."""
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.database import get_db
from app.models import Character, Novel, Location

router = APIRouter(prefix="/search", tags=["search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def search_page(
    request: Request,
    q: str = Query(default="", max_length=200),
    db: Session = Depends(get_db)
):
    results = {"characters": [], "novels": [], "locations": []} if not q else _do_search(q, db)
    return templates.TemplateResponse(
        request, "search.html",
        {"q": q, "results": results}
    )


@router.get("/api")
async def search_api(
    q: str = Query(default="", max_length=200),
    db: Session = Depends(get_db)
):
    """JSON endpoint for live search (used by the header search box)."""
    if not q or len(q) < 2:
        return {"results": []}
    results = _do_search(q, db)
    out = []
    for c in results["characters"][:5]:
        out.append({"type": "character", "name": c.name,
                    "subtitle": c.occupation or "", "url": f"/characters/{c.slug}"})
    for n in results["novels"][:3]:
        out.append({"type": "novel", "name": n.title_en,
                    "subtitle": str(n.year or ""), "url": f"/novels/{n.slug}"})
    for l in results["locations"][:2]:
        out.append({"type": "location", "name": l.name,
                    "subtitle": l.location_type or "", "url": f"/locations/{l.slug}"})
    return {"results": out}


def _do_search(q: str, db: Session) -> dict:
    pattern = f"%{q}%"

    characters = (
        db.query(Character)
        .filter(or_(
            Character.name.ilike(pattern),
            Character.birth_name.ilike(pattern),
            Character.occupation.ilike(pattern),
            Character.description_en.ilike(pattern),
        ))
        .order_by(Character.name)
        .limit(20)
        .all()
    )

    novels = (
        db.query(Novel)
        .filter(or_(
            Novel.title_en.ilike(pattern),
            Novel.title_fr.ilike(pattern),
            Novel.summary_en.ilike(pattern),
        ))
        .order_by(Novel.number)
        .limit(10)
        .all()
    )

    locations = (
        db.query(Location)
        .filter(or_(
            Location.name.ilike(pattern),
            Location.description_en.ilike(pattern),
        ))
        .order_by(Location.name)
        .limit(10)
        .all()
    )

    return {"characters": characters, "novels": novels, "locations": locations}
