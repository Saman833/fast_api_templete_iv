import uuid
from typing import Optional, List
from app.api.deps import Session
from app.competetive_programming.model.problem_creators import ProblemCreator


class ProblemCreatorRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pc_id: uuid.UUID) -> Optional[ProblemCreator]:
        return self.session.get(ProblemCreator, pc_id)

    def create(self, pc: ProblemCreator) -> ProblemCreator:
        self.session.add(pc)
        self.session.commit()
        self.session.refresh(pc)
        return pc

    def list_by_problem(self, problem_id: uuid.UUID) -> List[ProblemCreator]:
        return self.session.query(ProblemCreator).filter(ProblemCreator.problem_id == problem_id).all()
