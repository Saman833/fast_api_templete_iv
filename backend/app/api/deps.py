from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import TokenPayload, User
from app.affirmation.service.user_affirmation_service import UserAffirmationService
from app.affirmation.service.affirmation_service import AffirmationService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
from app.group.service.group_service import GroupService

def get_group_service(
    session: SessionDep
) -> GroupService:
    from app.group.repository.group_repo import GroupRepository
    repo= GroupRepository(session=session)
    group_service = GroupService(repo=repo)
    return group_service

def get_user_affirmation_service(session: SessionDep):
    from app.affirmation.repository.affirmation_repo import AffirmationRepo
    from app.affirmation.repository.user_affirmation_repo import UserAffirmationRepo
    
    user_affirmation_repo= UserAffirmationRepo(session=session)
    affirmation_repo= AffirmationRepo(session=session)
    user_affirmation_service = UserAffirmationService(user_affirmation_repo=user_affirmation_repo, affirmation_repo=affirmation_repo)
    return  user_affirmation_service

def get_affirmation_service(session: SessionDep):
    from app.affirmation.repository.affirmation_repo import AffirmationRepo
    from app.affirmation.repository.user_affirmation_repo import UserAffirmationRepo
    
    user_affirmation_repo= UserAffirmationRepo(session=session)
    affirmation_repo= AffirmationRepo(session=session)
    affirmation_service = AffirmationService(user_affirmation_repo=user_affirmation_repo, affirmation_repo=affirmation_repo)
    return  affirmation_service
UserAffirmationServiceDep=Annotated[UserAffirmationService,Depends(get_user_affirmation_service)]
AffirmationServiceDep=Annotated[AffirmationService,Depends(get_affirmation_service)]
GroupSer = Annotated[GroupService, Depends(get_group_service)]
 
