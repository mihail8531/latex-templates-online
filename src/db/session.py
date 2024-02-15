from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings import settings

engine = create_async_engine(
    settings.DB_URL, connect_args={"application_name": "latex-templates-rest"}
)
SessionMaker = async_sessionmaker(engine, expire_on_commit=False)


async def wrapped_session_maker() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

get_session = wrapped_session_maker