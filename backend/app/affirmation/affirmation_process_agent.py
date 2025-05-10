 
 
import time
import logging
from app.api.deps import get_user_affirmation_service, get_db

logger = logging.getLogger(__name__)
duration_time = 20 * 60 # 20 mins

def affirmation_process_agent():
    db_generator = get_db()
    session = next(db_generator)

    try:
        user_af_service = get_user_affirmation_service(session=session)
        while True:
            try:
                print("this a process run")
                logger.info("Running affirmation task...")
                user_af_service.process_scheduled_affirmations()
            except Exception as e:
                logger.error(f"Error running scheduled task: {e}")
            time.sleep(duration_time)
    finally:
        # Close session manually
        session.close()
        try:
            next(db_generator)
        except StopIteration:
            pass
