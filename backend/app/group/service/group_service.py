import uuid 
from app.group.schema.group_schema import GroupCreate
from app.group.model.group_model import Group
class GroupService: 
    def __init__(self, repo):
        self.repo = repo
    def create_new_group(self,*, owner_id:uuid.UUID,group:GroupCreate):
        group = Group.model_validate(group , update={"owner_id": owner_id})  
        group = self.repo.create_group(group)
        return group
