from typing import Type
from injector import Injector
import pytest

from app.business.action.user import create, show, update, delete, get_by_creds, list
from app.business.command.user import CreateUser
from app.business.schema.user import User, UserBaseFactory, UserProps, UserRegisterFactory, UsersRequest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.business.service.user import UserService
from app.core import Role
from app.core.database.postgres import db_creds
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from fastapi import FastAPI

from app.core.exception import InvalidCredentials
from app.core.hashing.bcrypt import Bcrypt
from app.core.model import Credentials, PageRequest
from app.domain.model.user import UserFilter
from app.domain.repository.user import UserEraser, UserReader, UserScope

SQLAlchemyMiddleware(app = FastAPI(), db_url = db_creds.get_pg_url())
        
injector = Injector()
service = injector.get(UserService)
reader = injector.get(UserReader)
eraser = injector.get(UserEraser)
scope = injector.get(UserScope)
cmd =  injector.get(CreateUser)
# cmd = CreateUser(service, reader)

@pytest.mark.asyncio
async def test_user_commands():
    async with db():
        create_data = UserRegisterFactory.build()
        created_model = await cmd.execute(create_data)
        
        assert isinstance(created_model, User)
        assert isinstance(created_model.id, int)
        