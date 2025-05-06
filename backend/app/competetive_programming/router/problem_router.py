from fastapi import APIRouter, Depends
from app.competetive_programming.model.problem import Problem
from app.api.deps import CurrentUser ,ProblemServiceDep
router = APIRouter(prefix="/problem", tags=["problem"])

@router.get("/{problem_id}")
def get_problem_by_id(problem_id, current_user:CurrentUser,problem_service: ProblemServiceDep):
    return problem_service.get_by_id(problem_id)

@router.post("/")
def create_problem(problem: Problem, current_user:CurrentUser,problem_service: ProblemServiceDep):
    return problem_service.create(problem)

@router.get("/")
def list_problems(current_user:CurrentUser , problem_service: ProblemServiceDep):
    return problem_service.list_all()
