from typing import Optional, List
from datetime import datetime, time
import uuid

from app.affirmation.model.user_affirmation_model import UserAffirmation
from app.affirmation.enums import UserAffirmationStatus
from app.affirmation.schema.user_affirmation_schema import (
    AffirmationOptIn,
    AffirmationSettingsUpdate,
    AffirmationSettingsBase
)
from app.affirmation.model.affirmation_model import (
    Affirmation
)
from app.affirmation.repository.affirmation_repo import (
    AffirmationRepo
)
from app.affirmation.repository.user_affirmation_repo import (
    UserAffirmationRepo
)
from app.models import (
    User
)
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class UserAffirmationService:

    def __init__(self, affirmation_repo: AffirmationRepo, user_affirmation_repo: UserAffirmationRepo):
        self.affirmation_repo = affirmation_repo
        self.user_affirmation_repo = user_affirmation_repo

    def opt_in_affirmation(self, *, user_id: uuid.UUID, affirmation_opt: AffirmationOptIn) -> User:
        user: User = self.user_affirmation_repo.opt_in_user_affirmation(user_id=user_id, affirmation_opt=affirmation_opt)
        if not user:
            raise HTTPException(status_code=500, detail="internal error, please try again")
        if not user.affirmation_opted:
            raise HTTPException(status_code=400, detail="you are not opted int yet")
        self.user_affirmation_repo.add_missing_user_affirmations_for_user(user.id)
        return user

    def opt_out_affirmation(self, *, user_id: uuid.UUID):
        user: User = self.user_affirmation_repo.opt_out_user_affirmation(user_id=user_id)
        if user.affirmation_opted:
            raise HTTPException(status_code=500, detail="some error happend while opting out , please redo it ")
        return user

    def update_affirmation_settings(self, user_id, user_affirmation_update: AffirmationSettingsUpdate):
        return self.user_affirmation_repo.update_user_affirmation_settings(user_id=user_id, user_affirmation_update=user_affirmation_update)

    def get_affirmation_settings(self, user_id: uuid.UUID) -> AffirmationSettingsBase:
        user = self.user_affirmation_repo.get_affirmation_settings(user_id=user_id)
        if user is None:
            raise ValueError(f"No settings found for user_id: {user_id}")
        settings_data = {
            key: getattr(user, key)
            for key in AffirmationSettingsBase.__fields__.keys()
            if hasattr(user, key)
        }
        return AffirmationSettingsBase(**settings_data)

    def is_affirmationed_today(self, user_id: uuid.UUID) -> bool:
        updated_at: Optional[datetime] = self.user_affirmation_repo.get_latest_updated_time_user(user_id=user_id)
        if updated_at is None:
            return False
        try:
            return updated_at.date() == datetime.utcnow().date()
        except Exception as e:
            logger.warning(f"Failed to check if affirmation was sent today for user {user_id}: {e}")
            raise

    def get_last_sending_session(self):
        return self.user_affirmation_repo.get_latest_udpdate_time_table()

    def update_user_affirmation_status(self, user_id: uuid.UUID, affirmation_id: uuid.UUID, status: str):
        self.user_affirmation_repo.update_user_affirmation_status(user_id, affirmation_id=affirmation_id, status=status)

    def deliver_affirmation(self, affirmation: Affirmation, user_id: uuid.UUID):
        response = {}
        response["status_code"] = 200
        return response

    def get_first_unsent_affirmation(self, user_id: uuid.UUID):
        result = self.user_affirmation_repo.get_first_unsent_affirmation(user_id=user_id)
        if not result:
            pass
        return result

    def get_users_scheduled_between(self, previous_time, now_time) -> Optional[List[User]]:
        return self.user_affirmation_repo.get_users_scheduled_between(previous_time=previous_time, now_time=now_time)

    def process_scheduled_affirmations(self):
        last_sending_dt = self.get_last_sending_session()
        now_dt = datetime.utcnow()
        if not last_sending_dt:
            last_sending_time = time(0, 0, 0)
        else:
            last_sending_time = last_sending_dt.time()
        now_time = now_dt.time()
        users_to_be_sent = self.get_users_scheduled_between(previous_time=last_sending_time, now_time=now_time)
        if not users_to_be_sent:
            return
        for user in users_to_be_sent:
            if self.is_affirmationed_today(user.id):
                continue
            user_af_recored: Optional[UserAffirmation] = self.get_first_unsent_affirmation(user_id=user.id)
            if not user_af_recored:
                continue
            affirmation_to_send = self.affirmation_repo.get_affirmation_by_id(user_af_recored.affirmation_id)
            if not affirmation_to_send:
                continue
            try:
                response = self.deliver_affirmation(affirmation_to_send, user.id)
                status_map = {
                    200: UserAffirmationStatus.SENT.value,
                    400: UserAffirmationStatus.BAD_REQUEST.value,
                    500: UserAffirmationStatus.SERVER_ERROR.value,
                }
                affirmation_status = status_map.get(response.get("status_code", 0), UserAffirmationStatus.FAIL.value)
                self.update_user_affirmation_status(user.id, affirmation_id=affirmation_to_send.id, status=affirmation_status)
            except Exception:
                pass
