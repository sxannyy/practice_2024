import pytest
from uuid import uuid4
from db.models import PortalRole
from conftest import create_test_auth_headers_for_user
from datetime import timedelta
import settings

@pytest.mark.asyncio
async def test_get_all_user_subs(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "hashedpassword",
        "roles": [PortalRole.ROLE_PORTAL_USER],
        "subscription": "aer",
    }
    await create_user_in_database(
        user_id=str(user_data["user_id"]),
        name=user_data["name"],
        surname=user_data["surname"],
        email=user_data["email"],
        is_active=user_data["is_active"],
        hashed_password=user_data["hashed_password"],
        roles=user_data["roles"],
        subscription=user_data["subscription"],
    )

    headers = create_test_auth_headers_for_user(user_data["email"])
    response = client.get("/user/get_all_user_subs/", headers=headers)
    
    data_from_resp = response.json()
    assert response.status_code == 200
    assert data_from_resp["subscription"] == user_data["subscription"]

@pytest.mark.asyncio
async def test_get_user_by_subs(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "hashedpassword",
        "roles": [PortalRole.ROLE_PORTAL_USER],
        "subscription": "aer",
    }
    await create_user_in_database(
        user_id=str(user_data["user_id"]),
        name=user_data["name"],
        surname=user_data["surname"],
        email=user_data["email"],
        is_active=user_data["is_active"],
        hashed_password=user_data["hashed_password"],
        roles=user_data["roles"],
        subscription=user_data["subscription"],
    )

    headers = create_test_auth_headers_for_user(user_data["email"])
    response = client.get("/user/get_user_by_subs/", params={"subscription": "aer"}, headers=headers)
    
    data_from_resp = response.json()
    assert response.status_code == 200
    assert len(data_from_resp) > 0
    assert data_from_resp[0]["subscription"] == user_data["subscription"]

@pytest.mark.asyncio
async def test_subscribe(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "hashedpassword",
        "roles": [PortalRole.ROLE_PORTAL_USER],
        "subscription": None,
    }
    await create_user_in_database(
        user_id=str(user_data["user_id"]),
        name=user_data["name"],
        surname=user_data["surname"],
        email=user_data["email"],
        is_active=user_data["is_active"],
        hashed_password=user_data["hashed_password"],
        roles=user_data["roles"],
        subscription=user_data["subscription"],
    )

    headers = create_test_auth_headers_for_user(user_data["email"])
    response = client.patch("/user/subscribe/", json={"subscription": "abc"}, headers=headers)
    
    data_from_resp = response.json()
    assert response.status_code == 422

    users_from_db = await get_user_from_database(str(user_data["user_id"]))
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["subscription"] is None

@pytest.mark.asyncio
async def test_unsubscribe(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "hashedpassword",
        "roles": [PortalRole.ROLE_PORTAL_USER],
        "subscription": "abc",
    }
    await create_user_in_database(
        user_id=str(user_data["user_id"]),
        name=user_data["name"],
        surname=user_data["surname"],
        email=user_data["email"],
        is_active=user_data["is_active"],
        hashed_password=user_data["hashed_password"],
        roles=user_data["roles"],
        subscription=user_data["subscription"],
    )

    headers = create_test_auth_headers_for_user(user_data["email"])
    response = client.patch(f"/user/unsubscribe/?subscription={user_data['subscription']}", headers=headers)
    
    data_from_resp = response.json()
    assert response.status_code == 200
    
    users_from_db = await get_user_from_database(str(user_data["user_id"]))
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["subscription"] is None