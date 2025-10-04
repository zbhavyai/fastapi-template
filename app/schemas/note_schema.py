import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class _FromORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class NoteCreateDTO(BaseModel):
    title: str = Field(..., max_length=255)
    content: str | None


class NoteUpdateDTO(BaseModel):
    title: str | None = Field(None, max_length=255)
    content: str | None = None


class NoteSummaryDTO(_FromORM):
    id: uuid.UUID
    title: str
    updatedAt: datetime = Field(validation_alias="updated_at")


class NoteDTO(_FromORM):
    id: uuid.UUID
    title: str
    content: str | None = None
    createdAt: datetime = Field(validation_alias="created_at")
    updatedAt: datetime = Field(validation_alias="updated_at")
