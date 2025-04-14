import uuid
import pytest
from sqlmodel import SQLModel, create_engine, Session

from app.group.model.group_model import Group
from app.group.schema.group_schema import GroupUpdate
from app.group.repository.group_repo import GroupRepository

# Setup test database
@pytest.fixture
def test_engine():
    return create_engine("sqlite:///:memory:", echo=False)


@pytest.fixture
def create_tables(test_engine):
    SQLModel.metadata.create_all(test_engine)


@pytest.fixture
def db_session(test_engine, create_tables):
    with Session(test_engine) as session:
        yield session


@pytest.fixture
def repo(db_session):
    return GroupRepository(session=db_session)


@pytest.fixture
def sample_group():
    return Group(id=uuid.uuid4(), name="Test Group", owner_id=uuid.uuid4())

 
def test_create_group(repo, sample_group):
    result = repo.create_group(group=sample_group)
    assert result is not None
    assert result.id == sample_group.id
 
 
def test_get_group_by_id(repo, sample_group):
    repo.create_group(sample_group)
    result = repo.get_group_by_id(group_id=sample_group.id)
    assert result is not None
    assert result.name == "Test Group"


def test_get_group_by_id_not_found(repo):
    result = repo.get_group_by_id(group_id=uuid.uuid4())
    assert result is None

 
def test_get_group_by_user_id(repo, sample_group):
    repo.create_group(sample_group)
    result = repo.get_group_by_user_id(user_id=sample_group.owner_id)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].id == sample_group.id


def test_get_group_by_user_id_none(repo):
    result = repo.get_group_by_user_id(user_id=uuid.uuid4())
    assert result == []


def test_update_group_info(repo, sample_group):
    repo.create_group(sample_group)
    update_data = GroupUpdate(id=sample_group.id, name="Updated Name")
    
    updated_group = repo.update_group_info(group_update=update_data, group=sample_group)
    
    assert updated_group.name == "Updated Name"
    assert updated_group.id == sample_group.id


def test_delete_group_by_id(repo, sample_group):
    repo.create_group(sample_group)
    deleted = repo.delete_group_by_id(group=sample_group)
    assert deleted is True

    # Confirm deletion
    result = repo.get_group_by_id(group_id=sample_group.id)
    assert result is None


def test_delete_group_by_id_invalid(repo):
    # Try deleting an unsaved group
    unsaved_group = Group(id=uuid.uuid4(), name="Ghost", owner_id=uuid.uuid4())
    deleted = repo.delete_group_by_id(group=unsaved_group)
    assert deleted is False
