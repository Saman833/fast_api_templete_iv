from app.competetive_programming.model.contest_problem import ContestProblem
from app.competetive_programming.repo.contest_problem_repo import ContestProblemRepo

class ContestProblemService:
    def __init__(self, cp_repo: ContestProblemRepo):
        self.cp_repo = cp_repo

    def create(self, cp: ContestProblem):
        return self.cp_repo.create(cp)

    def get_by_id(self, cp_id):
        return self.cp_repo.get_by_id(cp_id)
