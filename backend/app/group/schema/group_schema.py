from app.group.model.group_model import GroupBase
from sqlmodel import Field 
import uuid 
class GroupCreate(GroupBase):
    pass 
class GroupPublic(GroupBase):
    pass 
class GroupUpdate(GroupBase): 
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
