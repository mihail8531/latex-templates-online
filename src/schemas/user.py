from datetime import datetime
from pydantic import BaseModel, Field

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
    display_name: ShortStr
    name: ShortStr
    surname: ShortStr
    patronymic: ShortStr
    password: Password
