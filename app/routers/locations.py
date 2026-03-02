"""Locations router."""
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Location, Novel

router = APIRouter(prefix="/locations", tags=["locations"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def location_list(request: Request, db: Session = Depends(get_db)):
    locations = db.query(Location).order_by(Location.name).all()
    return templates.TemplateResponse(
        request, "locations/list.html",
        {"locations": locations}
    )


@router.get("/{slug}", response_class=HTMLResponse)
async def location_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.slug == slug).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Find novels whose setting mentions this location
    novels = (
        db.query(Novel)
        .filter(Novel.setting.ilike(f"%{location.name}%"))
        .order_by(Novel.number)
        .all()
    )

    return templates.TemplateResponse(
        request, "locations/detail.html",
        {"location": location, "novels": novels}
    )
