from fastapi import APIRouter

from app.api.routes import note_router, ping_router

api_router = APIRouter()
api_router.include_router(ping_router.router, prefix="/ping", tags=["ping"])
api_router.include_router(note_router.router, prefix="/v1/note", tags=["notes"])
