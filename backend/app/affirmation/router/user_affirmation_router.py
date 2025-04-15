"""
This module defines the API routes for managing user affirmations. It includes endpoints for opting in to receive daily affirmations, 
opting out, updating affirmation settings, and retrieving the current user's affirmation settings.

Routes:
    - POST /user-affirmation/opt-in: Opt the current user in to receiving daily affirmations.
    - DELETE /user-affirmation/opt-out: Opt the current user out of receiving daily affirmations.
    - PUT /user-affirmation/update: Update the user's affirmation settings.
    - GET /user-affirmation/: Retrieve the current user's affirmation settings.

Dependencies:
    - `current_user`: The currently authenticated user.
    - `affirmation_service`: Service layer for handling affirmation-related operations.

Schemas:
    - `AffirmationCreate`: Schema for creating a new affirmation.
    - `AffirmationUpdate`: Schema for updating an existing affirmation.
    - `AffirmationDetail`: Schema for detailed affirmation information.
    - `AffirmationOut`: Schema for outputting affirmation data.

Repositories:
    - `AffirmationRepo`: Repository for managing affirmations.
    - `UserAffirmationRepo`: Repository for managing user-specific affirmations.

Services:
    - `AffirmationService`: Service class for business logic related to affirmations. 
"""
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

router = APIRouter(prefix="/user-affirmation", tags=["user-affirmation"])

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
def update_user_affirmation_setings(
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
def get_user_affirmation_settings(
    *,
    current_user: CurrentUser,
    affirmation_service: AffirmationSer
):
    """
    gets user's affirmation settings.
    """
    return affirmation_service.get_affirmation_detail(owner_id=current_user.id)
