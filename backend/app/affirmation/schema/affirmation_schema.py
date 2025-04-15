from pydantic import BaseModel
from datetime import datetime

class AffirmationCreate(BaseModel):
    title: str
    content: str

class AffirmationOut(BaseModel):
    id: str
    title: str
    content: str

class UserAffirmationOut(BaseModel):
    user_id: str
    affirmation_id: str
    status: str
    sent_at: datetime | None = None