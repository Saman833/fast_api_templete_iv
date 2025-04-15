import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class Affirmation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    content: str 

