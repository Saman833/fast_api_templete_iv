import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class Affirmation(SQLModel, table=True):
    id:uuid.UUID  = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str =Field(min_length=4 , max_length=20)
    content: str =Field(min_length=10 , max_length=500)

