from pydantic import BaseModel
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str
    phone_no: str


class User(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class Login(UserBase):
    email: str
    password: str


