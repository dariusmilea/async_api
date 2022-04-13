from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True


class UserReadOnly(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

    class Config:
        orm_mode = True
