
from sqlmodel import select, text
from app.affirmation.model.affirmation_model import Affirmation 
from app.affirmation.model.user_affirmation_model import UserAffirmation 
from app.api.deps import SessionDep
from app.models import User
import uuid
from datetime import time 
from typing import List

class AffirmationRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_random_affirmation(self) -> Affirmation:
        statement = select(Affirmation).order_by(func.random()).limit(1)
        return self.session.exec(statement).first()

    def create_affirmation(self, affirmation: Affirmation):
        self.session.add(affirmation)
        self.session.commit()
        self.session.refresh(affirmation)
        return affirmation

class UserAffirmationRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, user_aff: UserAffirmation):
        self.session.add(user_aff)
        self.session.commit()
        self.session.refresh(user_aff)
        return user_aff
    
    def add_missing_user_affirmations_for_user(self, user_id: uuid.UUID):
        """
        Inserts missing affirmation records into the user_affirmation table
        for a specific user (user_id). Only affirmations that don't already exist
        for that user will be added.
        """
        query = """
        INSERT INTO user_affirmation (user_id, affirmation_id)
        SELECT :user_id, a.id
        FROM affirmation a
        WHERE NOT EXISTS (
            SELECT 1
            FROM user_affirmation ua
            WHERE ua.user_id = :user_id AND ua.affirmation_id = a.id
        )
        """
        self.session.exec(query, {"user_id": user_id})
        self.session.commit()
    def add_missing_user_affirmation_for_affirmation(self, affirmation_id: uuid.UUID):
        """
        Inserts missing user_affirmation records for a specific affirmation_id.
        Adds a record for every user who does not yet have this affirmation in the table.
        """
        query = """
        INSERT INTO user_affirmation (user_id, affirmation_id)
        SELECT u.id, :affirmation_id
        FROM "user" u
        WHERE NOT EXISTS (
            SELECT 1
            FROM user_affirmation ua
            WHERE ua.user_id = u.id AND ua.affirmation_id = :affirmation_id
        )
        """
        self.session.exec(query, {"affirmation_id": affirmation_id})
        self.session.commit()

    def get_first_unsent_affirmation(self, user_id: uuid.UUID):
        """
        Fetches the first unsent user_affirmation row for the given user_id using raw SQL.
        Assumes the 'status' column is a string and 'sent' indicates it has been sent.
        """
        query = """
        SELECT *
        FROM user_affirmation
        WHERE user_id = :user_id
        AND status != 'sent'
        LIMIT 1
        """
        result = self.session.exec(query, {"user_id": str(user_id)}).first()
        return result

    def update_user_affirmation_status(self, user_id: uuid.UUID, affirmation_id: uuid.UUID, status: str):
        """
        Updates the status field in the user_affirmation table
        for a specific (user_id, affirmation_id) pair.
        """
        query = """
        UPDATE user_affirmation
        SET status = :status
        WHERE user_id = :user_id AND affirmation_id = :affirmation_id
        """
        self.session.exec(
            text(query),
            {
                "user_id": str(user_id),
                "affirmation_id": str(affirmation_id),
                "status": status
            }
        )
        self.session.commit()

    def get_users_scheduled_between(self, previous_time: time, now_time: time) -> List[User]:
        """
        Returns all users who are opted-in for affirmations and have a schedule
        between `previous_time` and `now_time`.
        """
        statement = (
            select(User)
            .where(User.affirmation_opted == True)
            .where(User.affirmation_schedule != None)
            .where(User.affirmation_schedule.between(previous_time, now_time))
        )
        results = self.session.exec(statement).all()
        return results

            
 
