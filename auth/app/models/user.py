from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    auth_level: int = Field(default=0, ge=0, le=5)

    class Config:
        orm_mode = True


class UserReadOnly(BaseModel):
    id: str
    username: str
    email: EmailStr
    auth_level: int = Field(default=0, ge=0, le=5)

    class Config:
        orm_mode = True


class UserEdit(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    auth_level: int | None = Field(default=0, ge=0, le=5)

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str


class UserLoginResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    auth_level: str
    auth_token: str
