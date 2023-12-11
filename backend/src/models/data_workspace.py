from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.db.base import DeclarativeBase
from .data import Data
from .workspace import Workspace


class DataWorkspace(DeclarativeBase):
    __tablename__ = "data_workspace"

    data_id: Mapped[int] = mapped_column(ForeignKey(Data.id), primary_key=True)
    workspace_id: Mapped[int] = mapped_column(ForeignKey(Workspace.id), primary_key=True)
