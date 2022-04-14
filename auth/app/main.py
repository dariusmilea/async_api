import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException
from app.models.user import User, UserLogin, UserLoginResponse, UserReadOnly, UserEdit
from app.database.config import get_db
from app.services.user import (
    create_new_user,
    get_users,
    edit_user,
    delete_user,
    login_user,
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": secret}


@app.post("/users/", response_model=UserReadOnly)
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    try:
        created_user = await create_new_user(db, user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return created_user


@app.get("/users/", response_model=list[UserReadOnly])
async def list_users(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db)):
    users = await get_users(async_session=db, skip=offset, limit=limit)
    return users


@app.patch("/users/{id}", response_model=UserReadOnly)
async def update_user(id: str, user: UserEdit, db: AsyncSession = Depends(get_db)):
    try:
        updated_user = await edit_user(async_session=db, user=user, user_id=id)
        logging.warning(updated_user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return updated_user


@app.delete("/users/{id}", response_model=UserReadOnly)
async def remove_user(id: str, db: AsyncSession = Depends(get_db)):
    try:
        deleted_user = await delete_user(async_session=db, user_id=id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return deleted_user


@app.post("/login", response_model=UserLoginResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        logged_in_user = await login_user(async_session=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return logged_in_user
