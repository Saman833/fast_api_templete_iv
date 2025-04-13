from app.group.model.membership_model import (
    Membership,
    MembershipCreate,
    MembershipUpdate,
    MembershipPublic,
    MembershipList,
)
from sqlmodel import Session, select
class MembershipRepository:
    def __init__ (self, session: Session):
        self.session = session
    def create_membership(self, membership_in: MembershipCreate) -> Membership:
        db_membership = Membership.model_validate(membership_in)
        self.session.add(db_membership)
        self.session.commit()
        self.session.refresh(db_membership)
        return db_membership