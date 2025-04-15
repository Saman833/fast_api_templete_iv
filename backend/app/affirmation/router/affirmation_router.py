from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.affirmation.schema.affirmation_schema import (
    AffirmationCreate,
    AffirmationUpdate,
    AffirmationDetail,
    AffirmationOut
)
from app.affirmation.repository.affirmation_repo import (
    AffirmationRepo,
    UserAffirmationRepo
)
from app.affirmation.service.affirmation_service import AffirmationService
from app.api.deps import SessionDep, CurrentUser, AffirmationSer

router = APIRouter(prefix="/affirmations", tags=["affirmations"])


@router.post("/send/{user_id}", response_model=AffirmationOut)
def send_affirmation(user_id: str, db_session: SessionDep):
    """
    Send a daily affirmation to the specified user.
    """
    affirmation_repo = AffirmationRepo(db_session)
    user_aff_repo = UserAffirmationRepo(db_session)
    service = AffirmationService(affirmation_repo, user_aff_repo)
    return service.send_daily_affirmation(user_id)


@router.post("/opt-in", response_model=AffirmationDetail)
def opt_in_affirmation(
    *,
    current_user: CurrentUser,
    affirmation_data: AffirmationCreate,
    affirmation_service: AffirmationSer
):
    """
    Opt the current user in to receiving daily affirmations , will get time schedule as well ,   
    """
    return affirmation_service.opt_in_affirmation(
        owner_id=current_user.id,
        affirmation_request=affirmation_data
    )


@router.delete("/opt-out")
def opt_out_affirmation(
    *,
    current_user: CurrentUser,
    affirmation_service: AffirmationSer
):
    """
    Opt the current user out of receiving daily affirmations.
    """
    return affirmation_service.opt_out_affirmation(owner_id=current_user.id)


@router.put("/update", response_model=AffirmationDetail)
def update_affirmation_detail(
    *,
    current_user: CurrentUser,
    affirmation_update: AffirmationUpdate,
    affirmation_service: AffirmationSer
) :
    """
    Update the user's affirmation settings.
    """
    return affirmation_service.update_affirmation(
        owner_id=current_user.id,
        affirmation_request=affirmation_update
    )


@router.get("/", response_model=AffirmationDetail)
def get_affirmation_detail(
    *,
    current_user: CurrentUser,
    affirmation_service: AffirmationSer
):
    """
    gets user's affirmation settings.
    """
    return affirmation_service.get_affirmation_detail(owner_id=current_user.id)
