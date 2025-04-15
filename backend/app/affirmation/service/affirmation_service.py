from app.affirmation.domain.affirmation_domain import UserAffirmationEntity
from app.affirmation.model.user_affirmation_model import UserAffirmation
from datetime import datetime

class AffirmationService:
    def __init__(self, affirmation_repo, user_aff_repo):
        self.affirmation_repo = affirmation_repo
        self.user_aff_repo = user_aff_repo

    def send_daily_affirmation(self, user_id: str):
        affirmation = self.affirmation_repo.get_random_affirmation()
        user_aff = UserAffirmationEntity(user_id=user_id, affirmation_id=affirmation.id)
        user_aff.mark_sent()

        record = UserAffirmation(**user_aff.__dict__)
        self.user_aff_repo.create_or_update(record)

        # TODO: send notification (email, push, etc)
        return affirmation