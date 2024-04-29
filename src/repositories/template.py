from .repository import AlchemyIdRepository
from models.public import Template
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class TemplateRepository(AlchemyIdRepository[Template, int]):
    alchemy_model = Template

    