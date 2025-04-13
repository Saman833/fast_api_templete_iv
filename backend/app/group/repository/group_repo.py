from app.group.model.group_model import Group
from app.group.schema.group_schema import (
    GroupUpdate
)
from app.api.deps import SessionDep 
from sqlmodel import Session , select 
import uuid
class GroupRepository:
    def __init__(self, session:Session ):
        self.session = session


    def create_group(self, group: Group) -> Group| None:
        try  : 
            self.session.add(group)
            self.session.commit()
            self.session.refresh(group)
            return group 
        except Exception as e : 
            print ("error while creating :" ,e )


    def get_group_by_id(self,group_id=uuid.UUID) -> Group| None:
        try : 
            group =self.session.get(Group,group_id)
            return group 
        except Exception as e : 
            print ("while geting the data : " ,e )
            return None 
        

    def get_group_by_user_id(self,user_id) ->list[Group] | None : 
        try :
            statment =select(Group).where(Group.owner_id==user_id) 
            all_groups=self.session.exec(statment).all()
            return  all_groups
        except Exception as e : 
            print ("ERROR : while geting groups by user_id :" ,e)
            return None
        

    def update_group_info(self,group_update : GroupUpdate , group:Group) -> Group| None:
        update_dict = group_update.model_dump(exclude_unset=True)
        group.sqlmodel_update(update_dict)
        self.session.add(group)
        self.session.commit()
        self.session.refresh(group)
        return group
    

    def delete_group_by_id(self,group:Group) -> bool:
        try : 
            self.session.delete(group)
            self.session.commit()            
        except Exception as e : 
            print ("someting bad happend") 
            return False 
        return True 
 
