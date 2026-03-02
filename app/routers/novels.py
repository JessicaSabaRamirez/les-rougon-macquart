"""Novels router — index and individual novel pages."""
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Novel, CharacterAppearance, Character

router = APIRouter(prefix="/novels", tags=["novels"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def novel_list(request: Request, db: Session = Depends(get_db)):
    novels = db.query(Novel).order_by(Novel.number).all()
    return templates.TemplateResponse(
        request, "novels/list.html",
        {"novels": novels}
    )


@router.get("/{slug}", response_class=HTMLResponse)
async def novel_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    novel = db.query(Novel).filter(Novel.slug == slug).first()
    if not novel:
        raise HTTPException(status_code=404, detail="Novel not found")

    # Characters appearing in this novel
    appearances = (
        db.query(CharacterAppearance)
        .filter(CharacterAppearance.novel_id == novel.id)
        .join(Character)
        .order_by(CharacterAppearance.role, Character.name)
        .all()
    )

    return templates.TemplateResponse(
        request, "novels/detail.html",
        {
            "novel": novel,
            "appearances": appearances,
        }
    )
