from typing import ContextManager
import pytest
import pytest_asyncio
import contextlib
from app.core.database.postgres import async_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.model.user import User, user_factory
from app.domain.repository.user import UserEraser, UserWriter

@pytest_asyncio.fixture(name='session')
async def session() -> AsyncSession:
    async with async_session() as session:
        yield session
        
#PYTHONPATH=/code pytest /code/app/tests

async def temp_user(session: AsyncSession) -> User:
    user = user_factory.build()
    writer = UserWriter(session)
    id = await writer.create(user)
    user.id = id
    
    return user