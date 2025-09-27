from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str | None = None


class NoteCreateSchema(NoteBase):
    pass
