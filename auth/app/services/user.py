from asyncio.log import logger
import logging
from app.database.db_models.user import User as DBUSER
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


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
        hashed_password = str(hash(user.password))
        db_user = DBUSER(email=user.email, username=user.username, password=hashed_password)
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
