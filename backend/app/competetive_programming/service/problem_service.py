from app.competetive_programming.model.problem import Problem
from app.competetive_programming.repo.problem_repo import ProblemRepo

class ProblemService:
    def __init__(self, problem_repo: ProblemRepo):
        self.problem_repo = problem_repo

    def get_by_id(self, problem_id):
        return self.problem_repo.get_by_id(problem_id)

    def create(self, problem: Problem):
        return self.problem_repo.create(problem)

    def list_all(self):
        return self.problem_repo.list_all()
