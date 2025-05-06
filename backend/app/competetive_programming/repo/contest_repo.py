import uuid
from typing import Optional, List
from app.api.deps import Session
from app.competetive_programming.model.contest import Contest


class ContestRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, contest_id: uuid.UUID) -> Optional[Contest]:
        return self.session.get(Contest, contest_id)

    def create(self, contest: Contest) -> Contest:
        self.session.add(contest)
        self.session.commit()
        self.session.refresh(contest)
        return contest

    def list_all(self) -> List[Contest]:
        return self.session.query(Contest).all()
