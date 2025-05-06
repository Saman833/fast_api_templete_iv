from app.competetive_programming.model.problem_creators import ProblemCreator
from app.competetive_programming.repo.problem_creator_repo import ProblemCreatorRepo

class ProblemCreatorService:
    def __init__(self, pc_repo: ProblemCreatorRepo):
        self.pc_repo = pc_repo

    def create(self, pc: ProblemCreator):
        return self.pc_repo.create(pc)

    def get_by_problem_id(self, problem_id):
        return self.pc_repo.get_by_problem_id(problem_id)
