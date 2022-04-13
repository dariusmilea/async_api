from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException
from app.models.user import User, UserReadOnly
from app.database.config import get_db
from app.services.user import get_user_by_email, create_new_user, get_user_by_username

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users/", response_model=UserReadOnly)
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"Email {user.email} already registered")
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail=f"Username {user.username} already registered")

    created_user = await create_new_user(db, user=user)
    return created_user
