import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class AffirmationBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    content: Optional[str] = Field(default=None, max_length=255)

# SQLModel-based DB table
class Affirmation(AffirmationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)