import uuid
from datetime import datetime , time
import random
from app.models import User
from app.affirmation.model.affirmation_model import Affirmation
from app.affirmation.model.user_affirmation_model import UserAffirmation
from app.affirmation.repository.affirmation_repo import AffirmationRepo
from app.affirmation.repository.user_affirmation_repo import UserAffirmationRepo
from app.affirmation.service.affirmation_service import AffirmationService 
from app.affirmation.service.user_affirmation_service import UserAffirmationService 
from app.affirmation.schema.affirmation_schema import AffirmationCreate
from app.affirmation.schema.user_affirmation_schema import AffirmationOptIn
from app.affirmation.enums import UserAffirmationStatus
from app import crud
from app.core.security import verify_password
from app.models import User, UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from sqlmodel import Session



def get_aff_repo(db:Session):
    return AffirmationRepo(db) 

def get_user_aff_repo(db:Session):
    return UserAffirmationRepo(db)

def get_aff_service(db:Session):
    return AffirmationService(af_repo=get_aff_repo(db), user_af_repo=get_user_aff_repo(db)) 

def get_user_aff_service(db:Session):
    return UserAffirmationService(affirmation_repo=get_aff_repo(db), user_affirmation_repo=get_user_aff_repo(db))  

def random_affrimation() -> Affirmation:
    return Affirmation(
        id=uuid.uuid4(),
        title=f"TestTitle_{uuid.uuid4().hex[:6]}",  
        content="This is a random test content with at least 10 chars."
    )

def random_user(db:Session) -> User:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.create_user(session=db, user_create=user_in)
    return user 

def random_user_affrimation(db:Session):
    user = random_user(db)
    affirmation = random_affrimation()
    
    user_aff = UserAffirmation(
        user_id=user.id,           # user.id is a UUID, but the field is str
        affirmation_id=affirmation.id,  # affirmation.id is already a str
        status=UserAffirmationStatus.PENDING.value,
        # updated_at will default to datetime.utcnow
    )
    
    return user, affirmation, user_aff


def random_affirmation_create() -> AffirmationCreate:
    return AffirmationCreate(
        title=f"Affirmation {uuid.uuid4().hex[:6]}",
        content="You are doing great, keep pushing forward every day!"
    )




def random_opt_in() -> AffirmationOptIn:
    # Generate a random time between 6:00 and 22:00
    random_hour = random.randint(6, 22)
    random_minute = random.choice([0, 15, 30, 45])
    
    return AffirmationOptIn(
        affirmation_schedule=time(hour=random_hour, minute=random_minute)
    )
