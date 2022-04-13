from asyncio.log import logger
import logging
from app.database.db_models.user import User as DBUSER
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_user_by_id(async_session, user_id: str):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).filter(DBUSER.id == user_id))
        return result.scalars().first()


async def get_user_by_username(async_session, username: str):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).filter(DBUSER.username == username))
        return result.scalars().first()


async def get_user_by_email(async_session, email: str):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).where(DBUSER.email == email))
        return result.scalars().first()


async def get_users(async_session, skip: int = 0, limit: int = 100):
    async with async_session.begin():
        result = await async_session.execute(select(DBUSER).offset(skip).limit(limit))
        return result.scalars().all()


async def create_new_user(async_session, user: User):
    async with async_session.begin():
        hashed_password = hash(user.password)
        db_user = DBUSER(email=user.email, username=user.username, password=str(hashed_password))
        async_session.add_all([db_user])
        async_session.commit()
        return db_user
