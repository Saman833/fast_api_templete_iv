import uuid
import datetime
from typing import Optional, List, Literal
from sqlmodel import SQLModel, Field, Relationship 
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
class Problem(SQLModel, table=True):
    __tablename__ = "problem"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str = Field(max_length=255)
    slug: str = Field(max_length=255, unique=True)
    difficulty: DifficultyLevel
    description: str

    input_format: Optional[str] = None
    output_format: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    constraints: Optional[str] = None

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    contests: List["ContestProblem"] = Relationship(back_populates="problem")
    creators: List["ProblemCreator"] = Relationship(back_populates="problem")
