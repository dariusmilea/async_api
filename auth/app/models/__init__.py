from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str


class UserReadOnly(BaseModel):
    username: str
    email: str
    jwt_token: str
