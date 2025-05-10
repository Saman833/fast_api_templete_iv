
from app.affirmation.model.affirmation_model import (
    Affirmation, 
)

from app.affirmation.schema.affirmation_schema import (
    AffirmationCreate, 
)
from app.affirmation.repository.affirmation_repo import AffirmationRepo 
from app.affirmation.repository.user_affirmation_repo import UserAffirmationRepo 
class AffirmationService:
    def __init__(self, af_repo:AffirmationRepo, user_af_repo:UserAffirmationRepo):
        self.af_repo = af_repo 
        self.user_af_repo=user_af_repo
         
    def get_affirmation_by_id(self, affirmation_id):
        return self.af_repo.get_affirmation_by_id(affirmation_id)

    def create_affirmation(self, affirmation_create: AffirmationCreate) -> Affirmation:
        """
        this function should actually be named create_affirmation and add it to user_affrimation with all users 
        """
        affirmation_obj = Affirmation(**affirmation_create.dict())
        created_affirmation = self.af_repo.create_affirmation(affirmation_obj)
        self.user_af_repo.add_missing_user_affirmation_for_affirmation(affirmation_id=created_affirmation.id)
        
        return created_affirmation


     