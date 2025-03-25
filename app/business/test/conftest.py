import pytest
import pytest_asyncio
from app.core.database.postgres import async_session
from sqlalchemy.ext.asyncio import AsyncSession

@pytest_asyncio.fixture(name='session')
async def session() -> AsyncSession:
    async with async_session() as session:
        yield session
        
#PYTHONPATH=/code pytest /code/app/tests