import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class ContestProblem(SQLModel, table=True):
    __tablename__ = "contest_problem"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    contest_id: uuid.UUID = Field(foreign_key="contest.id")
    problem_id: uuid.UUID = Field(foreign_key="problem.id")
    display_order: int
    score: Optional[int] = None

    contest: Optional["Contest"] = Relationship(back_populates="problems")
    problem: Optional["Problem"] = Relationship(back_populates="contests")
