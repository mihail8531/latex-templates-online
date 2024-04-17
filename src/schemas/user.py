from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from schemas.fields import Login, Password, ShortStr


class User(BaseModel):
    login: Login
    display_name: ShortStr
    name: ShortStr
    surname: ShortStr
    patronymic: ShortStr
    creation_timestamp: datetime


class UserCreate(BaseModel):
    login: Login
    password: Password
    email: EmailStr
    name: ShortStr
    display_name: ShortStr
