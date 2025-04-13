import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep , group_service
from app.group.schema.group_schema import (
    GroupCreate,
    GroupPublic,
)
router = APIRouter(prefix="/group", tags=["group"])
@router.post("/", response_model=GroupPublic) 
def create_group(
    *,
    current_user: CurrentUser,
    group_in: GroupCreate,
    group_service = group_service
) -> Any:
    """
    Create new group.
    """
    group = group_service.create_new_group(owner_id=current_user.id,group=group_in)
    return group 