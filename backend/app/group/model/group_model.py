# app/group/models/group_model.py

import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Base class for shared fields
class GroupBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)


# SQLModel-based DB table
class Group(GroupBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")
