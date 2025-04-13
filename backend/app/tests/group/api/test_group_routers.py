import pytest
from httpx import AsyncClient
from fastapi import status
from uuid import uuid4

from app.main import app  # adjust if your app is in a different location
from app.group.schema.group_schema import GroupCreate
from app.group.model.group_model import Group

# Fake dependencies and setup utilities
@pytest.fixture
def test_user():
    return {
        "id": uuid4(),
        "email": "testuser@example.com",
        "username": "testuser"
    }

@pytest.fixture
def group_create_data():
    return {
        "name": "Test Group",
        "description": "This is a test group."
    }

@pytest.mark.asyncio
async def test_create_group(monkeypatch, test_user, group_create_data):
    async def mock_create_new_group(owner_id, group_in):
        return Group(
            id=uuid4(),
            owner_id=owner_id,
            name=group_in.name,
            description=group_in.description
        )

    # Patch the group_service dependency
    from app.api.deps import GroupSer
    monkeypatch.setattr(GroupSer, "create_new_group", mock_create_new_group)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/group/",
            json=group_create_data,
            headers={"Authorization": f"Bearer fake-token-for-{test_user['id']}"}
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == group_create_data["name"]
    assert data["description"] == group_create_data["description"]

@pytest.mark.asyncio
async def test_get_group(monkeypatch, test_user):
    test_group_id = uuid4()
    group_obj = Group(
        id=test_group_id,
        owner_id=test_user["id"],
        name="Existing Group",
        description="Existing Description"
    )

    async def mock_get_group_by_id(owner_id, group_id):
        assert owner_id == test_user["id"]
        assert group_id == test_group_id
        return group_obj

    # Patch the group_service dependency
    from app.api.deps import GroupSer
    monkeypatch.setattr(GroupSer, "get_group_by_id", mock_get_group_by_id)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            f"/group/{test_group_id}",
            headers={"Authorization": f"Bearer fake-token-for-{test_user['id']}"}
        )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == group_obj.name
    assert data["description"] == group_obj.description
