import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from app.affirmation.enums import UserAffirmationStatus
from datetime import datetime
class UserAffirmation(SQLModel, table=True):
    __tablename__ = "user_affirmation"   

    user_id:uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    affirmation_id:uuid.UUID = Field(foreign_key="affirmation.id", primary_key=True)
    status: str = Field(default=UserAffirmationStatus.PENDING.value)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )