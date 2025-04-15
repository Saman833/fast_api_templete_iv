import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class UserAffirmation(SQLModel, table=True):
    __table__="user_affiramtion"
    user_id: str = Field(primary_key=True)
    affirmation_id: str = Field(primary_key=True)
    status: str = Field(default="pending")  # pending, sent, failed

