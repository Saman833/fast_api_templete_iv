import uuid
from typing import Optional, List
from app.api.deps import Session
from app.competetive_programming.model.problem import Problem


class ProblemRepo:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, problem_id: uuid.UUID) -> Optional[Problem]:
        return self.session.get(Problem, problem_id)

    def create(self, problem: Problem) -> Problem:
        self.session.add(problem)
        self.session.commit()
        self.session.refresh(problem)
        return problem

    def get_by_slug(self, slug: str) -> Optional[Problem]:
        return self.session.query(Problem).filter(Problem.slug == slug).first()

    def list_all(self) -> List[Problem]:
        return self.session.query(Problem).all()
