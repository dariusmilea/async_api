from asyncio.log import logger
import logging
from app.database.db_models.user import User as DBUSER
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from app.services.jwt_handler import sign_JWT_token


async def _hash_password(password: str):
    hash = str(sha256(password.encode("utf-8")).hexdigest())
    return hash


async def get_user_by_id(async_session, user_id):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).filter(DBUSER.id == user_id))
        return result.scalars().first()


async def get_user_by_username(async_session, username):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).filter(DBUSER.username == username))
        return result.scalars().first()


async def get_user_by_email(async_session, email):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).where(DBUSER.email == email))
        return result.scalars().first()


async def get_users(async_session, skip, limit):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).offset(skip).limit(limit))
        return result.scalars().all()


async def create_new_user(async_session, user):
    db_user = await get_user_by_email(async_session, email=user.email)
    if db_user:
        raise Exception(f"Email {user.email} already registered!")
    db_user = await get_user_by_username(async_session, username=user.username)
    if db_user:
        raise Exception(f"Username {user.username} already registered!")
    async with async_session.begin():
        hashed_password = await _hash_password(user.password)
        db_user = DBUSER(email=user.email, username=user.username, password=hashed_password, auth_level=user.auth_level)
        async_session.add(db_user)
        async_session.commit()
        return db_user


async def edit_user(async_session, user, user_id):
    async with async_session.begin():
        db_user = await async_session.get(DBUSER, user_id)
        if not db_user:
            raise Exception(f"User with id {user_id} not found!")
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key == "password":
                value = str(hash(value))
            setattr(db_user, key, value)
        async_session.add(db_user)
        async_session.commit()
        async_session.refresh(db_user)
        return db_user


async def delete_user(async_session, user_id):
    async with async_session.begin():
        db_user = await async_session.get(DBUSER, user_id)
        if not db_user:
            raise Exception(f"User with id {user_id} not found!")
        await async_session.delete(db_user)
        async_session.commit()
        return db_user


async def login_user(async_session, user):
    if not user.username and not user.email:
        raise Exception(detail="Username or Email is required to login")
    elif user.username:
        user_db = await get_user_by_username(async_session=async_session, username=user.username)
        if not user_db:
            raise Exception(detail=f"User with username {user.username} not found")
    elif user.email:
        user_db = await get_user_by_email(async_session=async_session, username=user.email)
        if not user_db:
            raise Exception(detail=f"User with email {user.email} not found")
    pass_hash = await _hash_password(user.password)
    if pass_hash == user_db.password:
        return {
            **user_db.__dict__,
            "auth_token": sign_JWT_token(user_db.id),
        }
    else:
        raise Exception(detail=f"Wrong password!")
