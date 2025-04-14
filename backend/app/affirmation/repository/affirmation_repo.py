
from app.api.deps import SessionDep 
from sqlmodel import Session , select 
import uuid
from app.affirmation.model.affirmation_model import Affirmation
from app.affirmation.model.user_affirmation_model import UserAffirmation
from sqlalchemy.orm import aliased
from sqlalchemy import select, outerjoin
class affirmationRepository:
    def __init__(self, session:Session ):
        self.session = session


    def create_affirmation(self, affirmation: Affirmation) -> Affirmation| None:
        pass


    def get_affirmation_by_id(self,affirmation_id=uuid.UUID) -> Affirmation| None:
        
        pass 

    def create_recoreds


            
 
