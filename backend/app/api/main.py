from fastapi import APIRouter , FastAPI

from app.api.routes import items, login, private, users, utils
from app.core.config import settings
from app.group.api import group_routers 
from app.affirmation.router import affirmation_router,  user_affirmation_router 
api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(group_routers.router)
# api_router.include_router(affirmation_router.router)
api_router.include_router(user_affirmation_router.router)
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
