# app/affirmation/service/affirmation_service.py

from typing import Optional
from datetime import datetime
import uuid

from app.affirmation.repository.affirmation_repo import (
    AffirmationRepo,
    UserAffirmationRepo
)
from app.affirmation.schema.affirmation_schema import (
    AffirmationCreate,
    AffirmationUpdate,
    AffirmationOut,
    AffirmationDetail
)
from app.affirmation.domain.affirmation_entity import (
    AffirmationEntity,
    UserAffirmationEntity
)
from app.affirmation.model.affirmation_model import (
    Affirmation,
    UserAffirmation
)
from app.models import (
    User
)

class AffirmationService:
    """
    Handles core application logic for user affirmations.
    This class is designed to be used as a dependency in FastAPI routes.
    """

    def __init__(self, affirmation_repo: AffirmationRepo, user_affirmation_repo: UserAffirmationRepo):
        self.affirmation_repo = affirmation_repo
        self.user_affirmation_repo = user_affirmation_repo

    def send_daily_affirmation(self, user_id: str) -> AffirmationOut:
        """
        Retrieves a random affirmation and marks it as sent for the given user.
        Returns an AffirmationOut schema.
        """
        # 1. Get a random affirmation (domain entity).
        affirmation_entity = self.affirmation_repo.get_random_affirmation()
        if not affirmation_entity:
            # Handle case if no affirmations exist
            # This could raise an exception or return a default response
            raise ValueError("No affirmations available.")

        # 2. Create a new UserAffirmationEntity in 'sent' status.
        user_aff_entity = UserAffirmationEntity(
            user_id=user_id,
            affirmation_id=affirmation_entity.id
        )
        user_aff_entity.mark_sent()  # Sets status="sent", sent_at=now

        # 3. Persist or update in the database.
        self.user_affirmation_repo.create_or_update(user_aff_entity)

        # 4. Return the AffirmationOut schema.
        return AffirmationOut(**affirmation_entity.__dict__)
    def get_all_affirmation_ids(self) -> list[Affirmation.id]:
        return self.affirmation_repo.get_all_ids() 
    
    def create_new_user_affirmation_recordes(self , owner_id:uuid.UUID):
        affirmation_ids=self.get_all_affirmation_ids()
        for affirmation_id in affirmation_ids : 
            user_affirmation=UserAffirmation(affirmation_id=affirmation_id, user_id=owner_id , status="pending")
            self.user_affirmation_repo.create(user_affirmation)
    
    def opt_in_affirmation(self, owner_id: str, affirmation_request: AffirmationCreate) -> AffirmationDetail:
        """
        Opt the user in to receive affirmations, based on provided request data.
        Returns AffirmationDetail to summarize what has been stored.
        """
        # 1. Create a new Affirmation domain entity (if you want a unique Affirmation).
        new_aff_entity = AffirmationEntity(
             title=affirmation_request.title,
            content=affirmation_request.content
        )
        created_aff = self.affirmation_repo.create_affirmation(new_aff_entity)

        # 2. Create the corresponding UserAffirmation with status="pending" or "active".
        user_aff_entity = UserAffirmationEntity(
            user_id=owner_id,
            affirmation_id=created_aff.id,
            status="pending"
        )
        self.user_affirmation_repo.create_or_update(user_aff_entity)

        # 3. Return AffirmationDetail with user-specific info.
        return AffirmationDetail(
            id=created_aff.id,
            title=created_aff.title,
            content=created_aff.content,
            status=user_aff_entity.status,
            sent_at=user_aff_entity.sent_at
        )

    def opt_out_affirmation(self, owner_id: str):
        """
        Opt the user out of receiving affirmations.
        Implementation can vary based on domain rules—
        e.g., delete records, set status, etc.
        """
        # Example: set the user's affirmation status to 'inactive' or delete the record
        user_aff_records = self.user_affirmation_repo.get_user_affirmations(owner_id)
        for record in user_aff_records:
            # This method is hypothetical; handle how you remove or update the user’s records
            self.user_affirmation_repo.delete(record)
        return {"message": "User successfully opted out of affirmations."}

    def update_affirmation(self, owner_id: str, affirmation_request: AffirmationUpdate) -> AffirmationDetail:
        """
        Updates the user’s existing affirmation data. This might mean updating
        the underlying Affirmation (title/content) or the user’s association with it.
        """
        # 1. Retrieve existing user–affirmation record(s) in some custom way:
        user_aff_records = self.user.get_user_affirmations(owner_id)
        if not user_aff_records:
            raise ValueError("No existing affirmation found for this user.")

        # Example: update the first associated affirmation
        user_aff = user_aff_records[0]
        existing_aff = self.affirmation_repo.get_affirmation_by_id(user_aff.affirmation_id)
        if not existing_aff:
            raise ValueError("Affirmation record not found.")

        # 2. Update the domain entity
        updated_title = affirmation_request.title or existing_aff.title
        updated_content = affirmation_request.content or existing_aff.content
        existing_aff.title = updated_title
        existing_aff.content = updated_content

        self.affirmation_repo.update_affirmation(existing_aff)

        # 3. Return the updated detail
        return AffirmationDetail(
            id=existing_aff.id,
            title=existing_aff.title,
            content=existing_aff.content,
            status=user_aff.status,
            sent_at=user_aff.sent_at
        )

    def get_affirmation_setting_detail(self, owner_id: str) -> AffirmationDetail:
        """
        Retrieve the details of the user’s affirmation status and the affirmation content.
        """
        user_aff_records = self.user_affirmation_repo.get_user_affirmation(owner_id)
        if not user_aff_records:
            # This could raise an HTTPException or return a default.
            raise ValueError("No affirmations found for this user.")

        # For simplicity, assume the user has one main affirmation record
        user_aff = user_aff_records[0]
        aff_entity = self.affirmation_repo.get_affirmation_by_id(user_aff.affirmation_id)
        if not aff_entity:
            raise ValueError("Affirmation record not found.")

        return AffirmationDetail(
            id=aff_entity.id,
            title=aff_entity.title,
            content=aff_entity.content,
            status=user_aff.status,
            sent_at=user_aff.sent_at
        )
