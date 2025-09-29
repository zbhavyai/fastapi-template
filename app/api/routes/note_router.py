import logging
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.note_schema import NoteCreateDTO, NoteDTO, NoteSummaryDTO, NoteUpdateDTO
from app.service.note_service import NoteService

logger = logging.getLogger(__name__)
router = APIRouter()
note_service = NoteService()


@router.get("", status_code=status.HTTP_200_OK, response_model=list[NoteSummaryDTO])
async def list_notes(
    db: AsyncSession = Depends(get_db),
) -> list[NoteSummaryDTO]:
    logger.debug("list_notes")

    return await note_service.list_notes(db)


@router.get("/{note_id}", status_code=status.HTTP_200_OK, response_model=NoteDTO)
async def get_note_by_id(
    note_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> NoteDTO:
    logger.debug("get_note_by_id")

    return await note_service.get_note_by_id(db, note_id)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=NoteDTO)
async def create_note(
    note: NoteCreateDTO,
    db: AsyncSession = Depends(get_db),
) -> NoteDTO:
    logger.debug("create_note")

    return await note_service.create_note(db, note)


@router.patch("/{note_id}", status_code=status.HTTP_200_OK, response_model=NoteDTO)
async def update_note(
    note_id: uuid.UUID,
    note: NoteUpdateDTO,
    db: AsyncSession = Depends(get_db),
) -> NoteDTO:
    logger.debug("update_note")

    return await note_service.update_note(db, note_id, note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    logger.debug("delete_note")

    return await note_service.delete_note(db, note_id)
