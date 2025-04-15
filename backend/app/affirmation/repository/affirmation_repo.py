
from sqlmodel import select
from app.affirmation.model.affirmation_model import Affirmation 
from app.affirmation.model.user_affirmation_model import UserAffirmation 
from app.api.deps import SessionDep
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

    def create_or_update(self, user_aff: UserAffirmation):
        self.session.add(user_aff)
        self.session.commit()
        self.session.refresh(user_aff)
        return user_aff

    def get_users_to_notify(self, current_time) -> list[tuple[str, str]]:
        # This should join with user preferences; mock logic:
        return self.session.exec("SELECT user_id FROM user WHERE is_opted = true AND scheduled_time = :t", {"t": current_time}).all()


            
 
