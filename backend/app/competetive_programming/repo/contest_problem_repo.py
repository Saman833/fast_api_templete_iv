import uuid
from typing import Optional, List
from app.api.deps import Session
from app.competetive_programming.model.contest_problem import ContestProblem

class ContestProblemRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, cp_id: uuid.UUID) -> Optional[ContestProblem]:
        return self.session.get(ContestProblem, cp_id)

    def create(self, cp: ContestProblem) -> ContestProblem:
        self.session.add(cp)
        self.session.commit()
        self.session.refresh(cp)
        return cp

    def list_by_contest(self, contest_id: uuid.UUID) -> List[ContestProblem]:
        return self.session.query(ContestProblem).filter(ContestProblem.contest_id == contest_id).all()
