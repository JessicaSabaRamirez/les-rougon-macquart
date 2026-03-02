"""Timeline router — historical and personal events across the cycle."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Event

router = APIRouter(prefix="/timeline", tags=["timeline"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def timeline(request: Request, db: Session = Depends(get_db)):
    events = (
        db.query(Event)
        .options(joinedload(Event.novel), joinedload(Event.characters))
        .order_by(Event.year, Event.id)
        .all()
    )
    return templates.TemplateResponse(
        request, "timeline.html",
        {"events": events}
    )
