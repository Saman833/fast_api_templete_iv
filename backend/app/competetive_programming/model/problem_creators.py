import uuid
import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class ProblemCreator(SQLModel, table=True):
    __tablename__ = "problem_creators"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    problem_id: uuid.UUID = Field(foreign_key="problem.id")
    creator_id: uuid.UUID  # No FK to users table defined yet
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    problem: Optional["Problem"] = Relationship(back_populates="creators")
