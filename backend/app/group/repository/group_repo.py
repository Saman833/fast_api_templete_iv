from app.group.model.group_model import Group
from app.api.deps import SessionDep
class GroupRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create_group(self, group: Group) -> Group:
        self.session.add(group)
        self.session.commit()
        self.session.refresh(group)
        return group