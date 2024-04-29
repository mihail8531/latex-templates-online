from pydantic import BaseModel
from datetime import datetime

class TicketsSetBase(BaseModel):
    name: str
    description: str | None
    lua: str | None

class TicketsSetCreate(TicketsSetBase):
    pass

class TicketsSetHeader(TicketsSetBase):
    id: int
    author_id: int
    template_id: int
    creation_timestamp: datetime
