from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.affirmation.schema.user_affirmation_schema import (
    AffirmationOptIn,
    AffirmationSettingsUpdate,
    AffirmationSettingsBase,
)
from app.api.deps import CurrentUser, UserAffirmationServiceDep

router = APIRouter(prefix="/user-affirmation", tags=["user-affirmation"])


@router.post("/opt-in", response_model=AffirmationOptIn)
def opt_in_affirmation(
    *,
    current_user: CurrentUser,
    affirmation_opt_in: AffirmationOptIn,
    user_affirmation_service: UserAffirmationServiceDep
):
    """
    Opt the current user in to receiving daily affirmations , will get time schedule as well ,   
    """
    return user_affirmation_service.opt_in_affirmation(
        user_id=current_user.id,
        affirmation_opt=affirmation_opt_in
    )


@router.delete("/opt-out" , response_model=AffirmationSettingsBase)
def opt_out_affirmation(
    *,
    current_user: CurrentUser,
    user_affirmation_service: UserAffirmationServiceDep
):
    """
    Opt the current user out of receiving daily affirmations.
    """
    return user_affirmation_service.opt_out_affirmation(owner_id=current_user.id)


@router.put("/update", response_model=AffirmationSettingsBase)
def update_user_affirmation_setings(
    *,
    current_user: CurrentUser,
    affirmation_update: AffirmationSettingsUpdate,
    user_affirmation_service: UserAffirmationServiceDep
) :
    """
    Update the user's affirmation settings.
    """
    return user_affirmation_service.update_affirmation_settings(
        owner_id=current_user.id,
        affirmation_request=affirmation_update
    )


@router.get("/", response_model=AffirmationSettingsUpdate)
def get_user_affirmation_settings(
    *,
    current_user: CurrentUser,
    user_affirmation_service: UserAffirmationServiceDep
):
    """
    gets user's affirmation settings.
    """
    return user_affirmation_service.get_affirmation_settings(owner_id=current_user.id)
