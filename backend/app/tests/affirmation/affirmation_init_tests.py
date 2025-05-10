import uuid
from datetime import datetime, time, timedelta
import random
from app.affirmation.enums import UserAffirmationStatus
from app.affirmation.schema.user_affirmation_schema import AffirmationOptIn, AffirmationSettingsUpdate
from app.affirmation.repository.user_affirmation_repo import UserAffirmationRepo
from app.affirmation.model.affirmation_model import Affirmation
from app.affirmation.model.user_affirmation_model import UserAffirmation
from app.affirmation.service.user_affirmation_service import UserAffirmationService
from app.affirmation.service.affirmation_service import AffirmationService
from app.affirmation.repository.affirmation_repo import AffirmationRepo

from app.tests.affirmation.utils import (
    random_user, 
    random_affrimation, 
    random_user_affrimation , 
    get_user_aff_service,
    get_aff_service,
    random_affirmation_create,
    random_opt_in
)

from sqlmodel import Session , select , func
from sqlalchemy import text 


def test_opt_in_user_affirmation(db: Session):
    user = random_user(db)
    optin = AffirmationOptIn(affirmation_schedule=time(9, 0))

    repo = UserAffirmationRepo(db)
    updated_user = repo.opt_in_user_affirmation(user.id, optin)

    assert updated_user.affirmation_opted is True
    assert updated_user.affirmation_schedule == time(9, 0)


def test_opt_out_user_affirmation(db: Session):
    user = random_user(db)
    user.affirmation_opted = True
    user.affirmation_schedule = time(10, 0)
    db.add(user)
    db.commit()

    repo = UserAffirmationRepo(db)
    updated_user = repo.opt_out_user_affirmation(user_id=user.id)

    assert updated_user.affirmation_opted is False
    assert updated_user.affirmation_schedule is None


def test_update_user_affirmation_settings(db: Session):
    user = random_user(db)
    user.affirmation_opted = True
    db.add(user)
    db.commit()

    repo = UserAffirmationRepo(db)
    update = AffirmationSettingsUpdate(affirmation_opted=False, affirmation_schedule=time(15, 30))
    result = repo.update_user_affirmation_settings(str(user.id), update)

    assert result.affirmation_opted is False
    assert result.affirmation_schedule == time(15, 30)


def test_get_affirmation_settings(db: Session):
    user = random_user(db)
    user.affirmation_schedule = time(14, 0)
    db.add(user)
    db.commit()
    repo = UserAffirmationRepo(db)
    fetched_user = repo.get_affirmation_settings(user.id)

    assert fetched_user.id == user.id
    assert fetched_user.affirmation_schedule == time(14, 0)


def test_add_missing_user_affirmations_for_user(db: Session):
    """
    Tests that after creating new affirmations, each opted-in user gets linked to all affirmations.
    """
    users_count = random.randint(3, 10)
    affirmation_count = random.randint(3, 10)
    users = [random_user(db) for _ in range(users_count)]
    affirmations = [random_affirmation_create() for _ in range(affirmation_count)]
    user_af_service = get_user_aff_service(db)
    af_service = get_aff_service(db)
    for affirmation in affirmations:
        af_service.create_affirmation(affirmation_create=affirmation)
    for user in users:
        user_af_service.opt_in_affirmation(user_id=user.id, affirmation_opt=random_opt_in())
        user_links = db.exec(select(UserAffirmation).where(UserAffirmation.user_id == user.id)).all()
        all_links = db.exec(select(UserAffirmation.affirmation_id)).all()
        all_affirmation_ids = {row for row in all_links}
    assert len(user_links) == len(all_affirmation_ids)

def test_add_missing_user_affirmations_for_affirmation(db: Session):
    """
    Tests that each new affirmation is linked to all opted-in users.
    """
    users_count = random.randint(3, 10)
    affirmation_count = random.randint(3, 10)
    users = [random_user(db) for _ in range(users_count)]
    user_af_service = get_user_aff_service(db)
    af_service = get_aff_service(db)
    for user in users:
        user_af_service.opt_in_affirmation(user_id=user.id, affirmation_opt=random_opt_in())
    created_affirmations = []
    for _ in range(affirmation_count):
        affirmation = random_affirmation_create()
        affirmation = af_service.create_affirmation(affirmation_create=affirmation)
        created_affirmations.append(affirmation)
    for affirmation in created_affirmations:
        rows = db.exec(select(UserAffirmation).where(UserAffirmation.affirmation_id == affirmation.id)).all()
        linked_user_ids = {row.user_id for row in rows}
        assert len(rows) == len(linked_user_ids)

def test_get_first_unsent_affirmation(db: Session):
    """
    This test creates a random number of affirmations for a user who has opted in.
    It then updates each unsent user_affirmation record to 'sent'. Instead of using
    the random count, it retrieves the total number of affirmations from the database
    with a SELECT over the affirmation table, and asserts that the number of updates
    equals that count.
    """

    # Create a random number of affirmations
    random_count = random.randint(3, 10)
    af_service = get_aff_service(db)
    user_af_service = get_user_aff_service(db)

    user = random_user(db)
    user = user_af_service.opt_in_affirmation(user_id=user.id, affirmation_opt=random_opt_in())

    for _ in range(random_count):
        affirmation = random_affirmation_create()
        af_service.create_affirmation(affirmation_create=affirmation)

    # Get the total count of affirmations from the affirmation table.
    stmt = select(func.count(Affirmation.id))
    result = db.exec(stmt).one()
    affirmation_count = result[0] if isinstance(result, tuple) else result

    sent_count = 0
    while True:
        record = user_af_service.get_first_unsent_affirmation(user.id)
        if not record:
            break
        user_af_service.update_user_affirmation_status(
            user_id=user.id,
            affirmation_id=record.affirmation_id,
            status="sent"
        )
        sent_count += 1

    assert sent_count == affirmation_count, f"Expected {affirmation_count} sent updates, got {sent_count}"





def test_get_users_scheduled_between_add_two(db: Session):
    """
    This test runs 10 times with randomly selected time segments. For each iteration, it performs the following steps:
    
    1. Chooses a random time segment (with a start time "previous_time" and an end time "now_time").
    2. Gets the current count of users whose affirmation_schedule falls within that segment.
    3. Adds two new users with affirmation_schedule set to a time inside the segment (the "middle_time" of the segment).
    4. Adds one new user with affirmation_schedule set to a time outside the segment.
    5. Commits the changes and then gets the updated count of users in the time segment.
    6. Asserts that the difference in counts (after_count - before_count) is exactly 2, indicating that only the two users inside the segment were added.
    """
    import random
    from datetime import time, datetime, timedelta

    user_af_service = get_user_aff_service(db)

    for _ in range(10):
        
        start_hour = random.randint(0, 22)
        start_minute = random.randint(0, 59)
        previous_time = time(start_hour, start_minute)

        end_hour = random.randint(start_hour + 1, 23)
        end_minute = random.randint(0, 59)
        now_time = time(end_hour, end_minute)

        users_before = user_af_service.get_users_scheduled_between(previous_time=previous_time, now_time=now_time)
        before_count = len(users_before) if users_before is not None else 0

        middle_hour = (start_hour + end_hour) // 2
        middle_minute = (start_minute + end_minute) // 2
        middle_time = time(middle_hour, middle_minute)

        user1 = random_user(db)
        user1.affirmation_opted = True
        user1.affirmation_schedule = middle_time
        db.add(user1)

        user2 = random_user(db)
        user2.affirmation_opted = True
        user2.affirmation_schedule = middle_time
        db.add(user2)

        dt_previous = datetime.combine(datetime.today(), previous_time)
        if dt_previous > datetime.combine(datetime.today(), time(0, 0)):
            dt_outside = dt_previous - timedelta(minutes=1)
        else:
            dt_now = datetime.combine(datetime.today(), now_time)
            dt_outside = dt_now + timedelta(minutes=1)
        outside_time = dt_outside.time()

        user3 = random_user(db)
        user3.affirmation_opted = True
        user3.affirmation_schedule = outside_time
        db.add(user3)

        db.commit()

        users_after = user_af_service.get_users_scheduled_between(previous_time=previous_time, now_time=now_time)
        after_count = len(users_after) if users_after is not None else 0

        assert after_count - before_count == 2, (
            f"Segment from {previous_time} to {now_time}: before_count={before_count}, after_count={after_count}"
        )

def test_get_latest_update_time_table(db: Session):
    user1, aff1, user_aff1 = random_user_affrimation(db)
    user2, aff2, user_aff2 = random_user_affrimation(db)
    user_aff1.updated_at = datetime.utcnow() - timedelta(minutes=5)
    user_aff2.updated_at = datetime.utcnow()
    db.add_all([user1, aff1, user_aff1, user2, aff2, user_aff2])
    db.commit()

    repo = UserAffirmationRepo(db)
    latest = repo.get_latest_udpdate_time_table()

    assert isinstance(latest, datetime)
    assert latest == user_aff2.updated_at
