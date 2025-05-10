from sqlmodel import select, text, func
from app.affirmation.model.affirmation_model import Affirmation
from app.affirmation.model.user_affirmation_model import UserAffirmation
from app.affirmation.schema.user_affirmation_schema import AffirmationOptIn, AffirmationSettingsUpdate
from app.api.deps import Session
from app.models import User
import uuid
from datetime import time, datetime
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

user_affirmation_table_name = UserAffirmation.__tablename__

class UserAffirmationRepo:
    def __init__(self, session: Session):
        self.session = session
        self.user_affirmation_tb_name = user_affirmation_table_name

    def opt_in_user_affirmation(self, user_id: uuid.UUID, affirmation_opt: AffirmationOptIn) -> User:
        statement = select(User).where(User.id == user_id)
        user = self.session.exec(statement).one_or_none()
        if not user:
            raise BaseException(f"how is this possbible user_id is : {user_id}")
        update_dict = affirmation_opt.model_dump(exclude_unset=True)
        update_dict["affirmation_opted"] = True
        user.sqlmodel_update(update_dict)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def opt_out_user_affirmation(self, *, user_id: uuid.UUID):
        user: User | None = self.session.get(User, user_id)
        if not user:
            raise ValueError(f"User not found with id={user_id}")
        user.affirmation_opted = False
        user.affirmation_schedule = None
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user_affirmation_settings(
        self, user_id: str, user_affirmation_update: AffirmationSettingsUpdate
    ) -> Optional[AffirmationSettingsUpdate]:
        user = self.session.get(User, user_id)
        if not user:
            raise ValueError(f"User not found with id={user_id}")
        user.sqlmodel_update(user_affirmation_update)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user_affirmation_update

    def get_affirmation_settings(self, user_id: uuid.UUID):
        return self.session.get(User, user_id)

    def add_missing_user_affirmations_for_user(self, user_id: uuid.UUID):
        """
        here I had to use raw query for some mismatch of versions and .. 
        """
        try:
            sql = """
            INSERT INTO user_affirmation (user_id, affirmation_id, status)
            SELECT :user_id, a.id, 'pending'
            FROM affirmation a
            WHERE NOT EXISTS (
                SELECT 1 
                FROM user_affirmation ua
                WHERE ua.user_id = :user_id AND ua.affirmation_id = a.id
            )
            """
            self.session.execute(text(sql), {"user_id": str(user_id)})
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add missing affirmations for user {user_id}: {e}")
            raise

    def add_missing_user_affirmation_for_affirmation(self, affirmation_id: uuid.UUID):
        try:
            statement_existing = select(UserAffirmation.user_id).where(
                UserAffirmation.affirmation_id == affirmation_id
            )
            existing_user_ids = {row for row in self.session.exec(statement_existing).all()}
            statement_all = select(User.id).where(User.affirmation_opted == True)
            all_user_ids = [row for row in self.session.exec(statement_all).all()]
            missing_user_ids = [uid for uid in all_user_ids if uid not in existing_user_ids]
            if not missing_user_ids:
                return
            new_user_affirmations = [
                UserAffirmation(user_id=uid, affirmation_id=affirmation_id)
                for uid in missing_user_ids
            ]
            self.session.bulk_save_objects(new_user_affirmations)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to add missing affirmation for all users for affirmation {affirmation_id}: {e}")
            raise

    def get_first_unsent_affirmation(self, user_id: uuid.UUID) -> UserAffirmation:
        """
        Equivalent to:
        SELECT *
        FROM user_affirmation
        WHERE user_id = :user_id
          AND status != 'sent'
        LIMIT 1
        """
        try:
            statement = (
                select(UserAffirmation)
                .where(UserAffirmation.user_id == user_id)
                .where(UserAffirmation.status != "sent")
                .limit(1)
            )
            result = self.session.exec(statement).first()
            return result
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to get first unsent affirmation for user {user_id}: {e}")
            return None

    def update_user_affirmation_status(self, user_id: uuid.UUID, affirmation_id: uuid.UUID, status: str):
        record = self.session.get(UserAffirmation, (str(user_id), str(affirmation_id)))
        if record:
            record.status = status
            self.session.add(record)
            self.session.commit()

    def get_users_scheduled_between(self, previous_time: time, now_time: time) -> Optional[List[User]]:
        statement = (
            select(User)
            .where(User.affirmation_opted == True)
            .where(User.affirmation_schedule != None)
            .where(User.affirmation_schedule.between(previous_time, now_time))
        )
        try:
            results = self.session.exec(statement).all()
            return results
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to get users scheduled between {previous_time} and {now_time}: {e}")
            return None

    def get_latest_updated_time_user(self, user_id: uuid.UUID) -> Optional[datetime]:
        """
        Equivalent to:
          SELECT MAX(updated_at) AS latest_update
          FROM user_affirmation
          WHERE user_id = :user_id
        """
        try:
            statement = (
                select(func.max(UserAffirmation.updated_at))
                .where(UserAffirmation.user_id == user_id)
            )
            result = self.session.exec(statement).one_or_none()
            if result:
                return result[0]
            return None
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to get latest updated time for user {user_id}: {e}")
            return None

    def get_latest_udpdate_time_table(self) -> Optional[datetime]:
        """
        Equivalent to:
          SELECT MAX(user_affirmation.updated_at)
          FROM user_affirmation
        """
        try:
            result = self.session.exec(select(func.max(UserAffirmation.updated_at))).first()
            return result
        except Exception as e:
            self.session.rollback()
            logger.error(f"Failed to get latest update time from table: {e}")
            return None
