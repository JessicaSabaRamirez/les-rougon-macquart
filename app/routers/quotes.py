"""Quotes router — browseable quote gallery."""
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models import Quote, Novel

router = APIRouter(prefix="/quotes", tags=["quotes"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def quotes(
    request: Request,
    novel: str = Query(default=""),
    db: Session = Depends(get_db),
):
    q = (
        db.query(Quote)
        .options(joinedload(Quote.character), joinedload(Quote.novel))
    )
    if novel:
        q = q.join(Novel).filter(Novel.slug == novel)
    quotes_list = q.order_by(Quote.novel_id, Quote.id).all()

    novels = db.query(Novel).order_by(Novel.number).all()
    return templates.TemplateResponse(
        request, "quotes.html",
        {"quotes": quotes_list, "novels": novels, "active_novel": novel}
    )
