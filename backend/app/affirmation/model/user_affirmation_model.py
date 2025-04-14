import uuid
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class UserAffirmation(SQLModel, table=True):
    __table__="user_affiramtion"
    affirmation_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: str = Field(min_length=1, max_length=10)
# add a defult status , 
class AffirmationStatus():
    pass


# status in user_affirmation 
# time in user 