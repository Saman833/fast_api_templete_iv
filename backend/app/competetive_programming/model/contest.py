import uuid
import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Contest(SQLModel, table=True):
    __tablename__ = "contest"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(max_length=255)
    description: Optional[str] = None
    start_time: datetime.datetime
    end_time: datetime.datetime
    is_active: bool = Field(default=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    problems: List["ContestProblem"] = Relationship(back_populates="contest")
