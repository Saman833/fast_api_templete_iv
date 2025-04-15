from app.affirmation.repository.affirmation_repo import UserAffirmationRepo
from app.affirmation.model.affirmation_model import Affirmation
from app.api.deps import UserAffirmationRepoD
from datetime import datetime
from app.affirmation.service.affirmation_service import AffirmationService
session=None

def sent_affirmation(repo: UserAffirmationRepo):
    repo=UserAffirmationRepo(session) 
    af_service=AffirmationService(repo)
    last_sening_session_time=repo.get_last_sending_session()
    now_time=datetime.now()
    users_to_be_sent=repo.get_users_scheduled_between(last_sening_session_time,now_time=now_time)
    for user in users_to_be_sent : 
        if af_service.user_recived_today() :  ### this very important line , 
            # if user change thier schulde after they recive one affrimation today , we should avoid sending any other affirmation for that day 
            continue

        affirmation_to_send: Affirmation =repo.get_first_unsent_affirmation(user_id=user.id)
        if not affirmation_to_send : 
            pass # TODO there should be some oertaion here like adding more affiration 
        response=af_service.send_affirmation(affirmation_to_send,user.id)
        affirmation_status="pending"

        match response.status_code:
            case 200:
                affirmation_status = "sent"
            case 400:
                affirmation_status = "bad_request" 
            case 500:
                affirmation_status = "server_error"
            case _:
                affirmation_status = "fail"
         
        repo.update_user_affirmation_status(user.id,affirmation_id=affirmation_to_send.id,status=affirmation_status)


