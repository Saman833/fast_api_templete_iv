from sqlmodel import SQLModel, Field

class AffirmationCreate(SQLModel):
    title: str
    content: str 