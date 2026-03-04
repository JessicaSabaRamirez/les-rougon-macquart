"""
Les Rougon-Macquart — Companion App
FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import os

from app.database import init_db
from app.routers import characters, novels, locations, search, timeline, quotes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Les Rougon-Macquart",
    description="Interactive companion to Zola's twenty-novel cycle",
    lifespan=lifespan,
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(characters.router)
app.include_router(novels.router)
app.include_router(locations.router)
app.include_router(search.router)
app.include_router(timeline.router)
app.include_router(quotes.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page — the genealogy tree."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/genealogy", response_class=HTMLResponse)
async def genealogy(request: Request):
    """Full genealogy page — all family-branch characters with pan/zoom."""
    return templates.TemplateResponse(request, "genealogy.html")


@app.get("/health")
async def health():
    return {"status": "ok"}
