import uuid
import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock

from app.group.schema.group_schema import GroupCreate, GroupUpdate
from app.group.model.group_model import Group
from app.group.service.group_service import GroupService 


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_repo):
    return GroupService(repo=mock_repo)


@pytest.fixture
def fake_group():
    return Group(id=uuid.uuid4(), name="Test Group", owner_id=uuid.uuid4())


def test_check_user_access_same_user(service):
    user_id = uuid.uuid4()
    assert service.check_user_access(user_id=user_id, group_owner_id=user_id) is True 


def test_check_user_access_different_user(service):
    assert service.check_user_access(user_id=uuid.uuid4(), group_owner_id=uuid.uuid4()) is False


def test_create_new_group(service, mock_repo):
    owner_id = uuid.uuid4()
    group_data = GroupCreate(name="New Group")
    
    service.create_new_group(owner_id=owner_id, group_in=group_data)
    
    assert mock_repo.create_group.called
    created_group = mock_repo.create_group.call_args[1]['group']
    assert created_group.owner_id == owner_id
    assert created_group.name == "New Group"


def test_get_group_by_id_success(service, mock_repo, fake_group):
    mock_repo.get_group_by_id.return_value = fake_group

    group = service.get_group_by_id(owner_id=fake_group.owner_id, group_id=fake_group.id)

    assert group == fake_group
    assert mock_repo.get_group_by_id.called


def test_get_group_by_id_not_found(service, mock_repo):
    mock_repo.get_group_by_id.return_value = None
    with pytest.raises(HTTPException) as e:
        service.get_group_by_id(owner_id=uuid.uuid4(), group_id=uuid.uuid4())
    assert e.value.status_code == 300


def test_get_group_by_id_access_denied(service, mock_repo, fake_group):
    mock_repo.get_group_by_id.return_value = fake_group
    wrong_user_id = uuid.uuid4()
    
    with pytest.raises(HTTPException) as e:
        service.get_group_by_id(owner_id=wrong_user_id, group_id=fake_group.id)
    assert e.value.status_code == 400


def test_get_group_by_user_id(service, mock_repo):
    user_id = uuid.uuid4()
    mock_repo.get_group_by_user_id.return_value = [Group(id=uuid.uuid4(), name="G", owner_id=user_id)]

    result = service.get_group_by_user_id(owner_id=user_id)

    assert isinstance(result, list)
    assert mock_repo.get_group_by_user_id.called


def test_delet_group_by_id_success(service, mock_repo, fake_group):
    mock_repo.get_group_by_id.return_value = fake_group
    mock_repo.delete_group_by_id.return_value = True

    result = service.delet_group_by_id(owner_id=fake_group.owner_id, group_id=fake_group.id)

    assert result == fake_group
    assert mock_repo.delete_group_by_id.called


def test_delet_group_by_id_failure(service, mock_repo, fake_group):
    mock_repo.get_group_by_id.return_value = fake_group
    mock_repo.delete_group_by_id.return_value = False

    with pytest.raises(HTTPException) as e:
        service.delet_group_by_id(owner_id=fake_group.owner_id, group_id=fake_group.id)
    assert e.value.status_code == 500


def test_update_group_by_id(service, mock_repo, fake_group):
    mock_repo.get_group_by_id.return_value = fake_group
    update_data = GroupUpdate(id=fake_group.id, name="Updated")

    service.update_group_by_id(owner_id=fake_group.owner_id, group_update=update_data)

    assert mock_repo.update_group_info.called
