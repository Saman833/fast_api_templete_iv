from app.affirmation.repository.affirmation_repo import AffirmationRepository 
from app.affirmation.repository.affirmation_repo import UserAffirmationRepository 

class AffirationService: 
    def __init__ (self,af_repo : AffirmationRepository , user_af_repo: UserAffirmationRepository) : 
        self.af_repo=af_repo
        self.user_af_repo=user_af_repo
        pass 
    def send_an_aformation(user_id : uuid.UUID) :
        raise         
