from logging import getLogger
from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.user import _create_new_user
from api.actions.user import _delete_user
from api.actions.user import _get_user_by_id
from api.actions.user import _update_user
from api.actions.user import _get_user_by_subs

from api.schemas import DeleteUserResponse, ShowSubs
from api.schemas import ShowUser
from api.schemas import UpdatedUserResponse
from api.schemas import UpdateUserRequest
from api.schemas import UserCreate

from api.actions.auth import get_current_user_from_token

from db.models import User
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()

@user_router.post("/create_user/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/delete_user/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if user_for_deletion != user_id(
    target_user=user_for_deletion,
    current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)

@user_router.get("/get_user_by_id/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user

@user_router.get("/get_all_user_subs/", response_model=ShowSubs)
async def get_all_user_subs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowSubs:
    user = await _get_user_by_id(current_user.user_id, db)
    if user.subscription is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {current_user.user_id} has no subscriptions."
        )
    return user

@user_router.get("/get_user_id/", response_model=ShowUser)
async def get_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(current_user.user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {current_user.user_id} not found."
        )
    return user

@user_router.get("/get_user_by_subs/", response_model=List[ShowSubs])
async def get_user_by_subs(
    subscription: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> List[ShowSubs]:
    user = await _get_user_by_subs(subscription, db)
    if user == []:
        raise HTTPException(
            status_code=404, detail=f"User with such subs not found."
        )
    return user

@user_router.patch("/update_user_by_id/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)