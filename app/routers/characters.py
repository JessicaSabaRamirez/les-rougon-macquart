"""Characters router — list and individual character pages."""
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.database import get_db
from app.models import Character, CharacterRelation, CharacterAppearance, Novel

router = APIRouter(prefix="/characters", tags=["characters"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
async def character_list(request: Request, db: Session = Depends(get_db)):
    characters = (
        db.query(Character)
        .order_by(Character.generation, Character.name)
        .all()
    )
    return templates.TemplateResponse(
        request, "characters/list.html",
        {"characters": characters}
    )


@router.get("/api/landing-tree")
async def landing_tree_data(db: Session = Depends(get_db)):
    """Return JSON data for the landing page genealogy SVG."""
    chars = (
        db.query(Character)
        .filter(Character.featured_on_landing == True)
        .order_by(Character.generation, Character.tree_x)
        .all()
    )

    # Build relations between featured characters only
    featured_ids = {c.id for c in chars}
    relations = (
        db.query(CharacterRelation)
        .filter(
            CharacterRelation.character_a_id.in_(featured_ids),
            CharacterRelation.character_b_id.in_(featured_ids),
            CharacterRelation.relation_type.in_(["parent", "spouse", "union"])
        )
        .all()
    )

    char_data = []
    for c in chars:
        # Get novels this character appears in
        appearances = (
            db.query(CharacterAppearance)
            .filter(CharacterAppearance.character_id == c.id)
            .join(Novel)
            .all()
        )
        novel_titles = [a.novel.title_en for a in appearances]

        char_data.append({
            "id": c.slug,
            "name": c.name,
            "role": c.occupation,
            "branch": c.branch or "other",
            "generation": c.generation,
            "description_en": c.description_en,
            "description_fr": c.description_fr,
            "novels": novel_titles,
            "image_url": c.image_url,
            "x": c.tree_x,
            "y": c.tree_y,
            "url": f"/characters/{c.slug}",
        })

    rel_data = []
    slug_map = {c.id: c.slug for c in chars}
    for r in relations:
        rel_data.append({
            "from": slug_map.get(r.character_a_id),
            "to": slug_map.get(r.character_b_id),
            "type": r.relation_type,
        })

    return {"characters": char_data, "relations": rel_data}


@router.get("/{slug}", response_class=HTMLResponse)
async def character_detail(slug: str, request: Request, db: Session = Depends(get_db)):
    character = db.query(Character).filter(Character.slug == slug).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    # Relations — load both directions
    relations_a = (
        db.query(CharacterRelation)
        .filter(CharacterRelation.character_a_id == character.id)
        .all()
    )
    related_chars = []
    for rel in relations_a:
        other = db.query(Character).filter(Character.id == rel.character_b_id).first()
        if other:
            related_chars.append({
                "character": other,
                "relation_type": rel.relation_type,
                "description": rel.description,
            })

    # Novel appearances
    appearances = (
        db.query(CharacterAppearance)
        .filter(CharacterAppearance.character_id == character.id)
        .join(Novel)
        .order_by(Novel.number)
        .all()
    )

    return templates.TemplateResponse(
        request, "characters/detail.html",
        {
            "character": character,
            "relations": related_chars,
            "appearances": appearances,
        }
    )
