from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings
from app.group.api import group_routers 
from app.competetive_programming.router import contest_reuter , problem_router

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(contest_reuter.router)
api_router.include_router(problem_router.router)
api_router.include_router(group_routers.router)
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
