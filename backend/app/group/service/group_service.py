import uuid 
from app.group.schema.group_schema import(
    GroupCreate , 
    GroupUpdate )
from app.group.model.group_model import Group
from app.group.repository.group_repo import GroupRepository
from app.group.domain.group_domain import GroupDomain
from fastapi import APIRouter, HTTPException 
class GroupService: 
    def __init__(self, repo:GroupRepository):
        self.repo = repo
    def check_user_access(self, * , user_id : uuid.UUID , group_owner_id:uuid.UUID) -> bool: 

        if user_id==group_owner_id : 
            return True 
        return False  
    def create_new_group(self,*, owner_id:uuid.UUID,group_in:GroupCreate) -> Group :

        group = Group.model_validate(group_in, update={"owner_id": str(owner_id)})
                   
        group = self.repo.create_group(group=group)
        if not group : 
            raise HTTPException(status_code=500 , detail="the system was not able to process your request")
        return group 

    def get_group_by_id(self,* , owner_id:uuid.UUID , group_id:uuid.UUID) -> Group:

        group=self.repo.get_group_by_id(group_id=group_id)
        if not group : 
            raise HTTPException(status_code=300, detail="there is not group with this ID ") 
        if not self.check_user_access(user_id=owner_id ,group_owner_id=group.owner_id): 
            raise HTTPException(status_code=400, detail="access denied")
        return group 
    
    def get_group_by_user_id(self,owner_id:uuid.UUID)-> list[Group] | None:

        groups = self.repo.get_group_by_user_id(user_id=owner_id)
        return groups
    
    def delet_group_by_id(self,*, owner_id:uuid.UUID , group_id:uuid.UUID):
        group=self.get_group_by_id(owner_id=owner_id , group_id=group_id) 
        is_deleted=self.repo.delete_group_by_id(group=group)
        if not is_deleted : 
            raise HTTPException(status_code=500 , detail="delete was not successful")
        return group 
    def update_group_by_id(self , owner_id:uuid.UUID , group_update:GroupUpdate) -> Group: 
        group=self.get_group_by_id(group_id=group_update.id , owner_id=owner_id) 
        self.repo.update_group_info(group=group, group_update=group_update) 
