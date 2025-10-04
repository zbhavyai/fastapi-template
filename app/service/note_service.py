import logging
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note_model import Note
from app.schemas.note_schema import NoteCreateDTO, NoteSummaryDTO, NoteUpdateDTO

logger = logging.getLogger(__name__)


class NoteService:
    async def list_notes(
        self,
        db: AsyncSession,
    ) -> list[NoteSummaryDTO]:
        logger.info("list_notes")

        result = await db.execute(select(Note).order_by(Note.updated_at.desc()))
        return [NoteSummaryDTO.model_validate(r) for r in result.scalars()]

    async def get_note_by_id(
        self,
        db: AsyncSession,
        note_id: uuid.UUID,
    ) -> Note:
        logger.info("get_note_by_id: %s", note_id)

        result = await db.execute(select(Note).where(Note.id == note_id))

        try:
            return result.scalar_one()

        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    async def create_note(
        self,
        db: AsyncSession,
        payload: NoteCreateDTO,
    ) -> Note:
        logger.info("create_note: %s", payload)

        note = Note(title=payload.title, content=payload.content)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    async def update_note(
        self,
        db: AsyncSession,
        note_id: uuid.UUID,
        payload: NoteUpdateDTO,
    ) -> Note:
        logger.info("update_note: %s", note_id)

        result = await db.execute(select(Note).where(Note.id == note_id))
        try:
            note = result.scalar_one()
            data = payload.model_dump(exclude_unset=True)
            for k, v in data.items():
                setattr(note, k, v)

            await db.commit()
            await db.refresh(note)
            return note

        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    async def delete_note(
        self,
        db: AsyncSession,
        note_id: uuid.UUID,
    ) -> None:
        logger.info("delete_note: %s", note_id)

        result = await db.execute(select(Note).where(Note.id == note_id))
        try:
            note = result.scalar_one()
            await db.delete(note)
            await db.commit()

        except NoResultFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
