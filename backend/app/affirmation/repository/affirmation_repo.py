from app.affirmation.model.user_affirmation_model import UserAffirmation 
from app.api.deps import Session
from app.models import User
import uuid
from datetime import time ,datetime
from typing import List , Optional

from app.affirmation.model.affirmation_model import (
    Affirmation,
) 
from app.affirmation.schema.affirmation_schema import (
    AffirmationCreate,
)
class AffirmationRepo():
    def __init__(self, session: Session):
        self.session = session

    def get_affirmation_by_id(self, affirmation_id: uuid.UUID) -> Optional[Affirmation]:
        return self.session.get(Affirmation, affirmation_id)

    def create_affirmation(self, affirmation: Affirmation) -> Affirmation:
        """ creates and retunrn the new affirmation """

        self.session.add(affirmation)
        self.session.commit()
        self.session.refresh(affirmation)
        return affirmation
