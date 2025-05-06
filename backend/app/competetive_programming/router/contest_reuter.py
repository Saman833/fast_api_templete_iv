from fastapi import APIRouter, Depends
from fastapi import APIRouter, Depends
from app.competetive_programming.model.contest import Contest
from app.api.deps import CurrentUser ,ContestServiceDep


router = APIRouter(prefix="/contest", tags=["contest"])

@router.get("/{contest_id}")
def get_contest_by_id(contest_id, contest_service: ContestServiceDep , current_user: CurrentUser):
    return contest_service.get_by_id(contest_id)

@router.post("/")
def create_contest(contest: Contest, contest_service: ContestServiceDep , current_user: CurrentUser):
    return contest_service.create(contest)

@router.get("/")
def list_contests(contest_service: ContestServiceDep , current_user: CurrentUser):
    return contest_service.list_all()
