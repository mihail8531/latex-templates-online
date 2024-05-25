from .alchemy import AlchemyIdRepository
from models.public import Template
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class TemplateRepository(AlchemyIdRepository[Template, int]):
    alchemy_model = Template

    async def get_full(self, template: Template) -> Template:
        await template.awaitable_attrs.workspace
        await template.awaitable_attrs.tickets_sets
        return template
