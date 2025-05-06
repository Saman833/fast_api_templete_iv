from app.competetive_programming.model.contest import Contest
from app.competetive_programming.repo.contest_repo import ContestRepo

class ContestService:
    def __init__(self, contest_repo: ContestRepo):
        self.contest_repo = contest_repo

    def get_by_id(self, contest_id):
        return self.contest_repo.get_by_id(contest_id)

    def create(self, contest: Contest):
        return self.contest_repo.create(contest)

    def list_all(self):
        return self.contest_repo.list_all()
