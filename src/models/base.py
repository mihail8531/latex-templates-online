from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

class Base(DeclarativeBase):
    __abstract__ = True

class BaseIdModel(Base):
    __abstract__ = True

    id: Mapped[Any]
