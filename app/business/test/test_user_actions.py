from typing import Type
import pytest

from app.business.action.user import create, show, update, delete, get_by_creds, list
from app.business.schema.user import User, UserBaseFactory, UserProps, UserRegisterFactory, UsersRequest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.core import Role
from app.core.database.postgres import db_creds
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from fastapi import FastAPI

from app.core.exception import InvalidCredentials
from app.core.hashing.bcrypt import Bcrypt
from app.core.model import Credentials, PageRequest
from app.domain.model.user import UserFilter
from app.domain.repository.user import UserReader

SQLAlchemyMiddleware(app = FastAPI(), db_url = db_creds.get_pg_url())
        
@pytest.mark.asyncio
async def test_user_actions():
    async with db():
        create_data = UserRegisterFactory.build()
        creds = Credentials(email=create_data.email, password=create_data.password)
        created_model = await create(create_data)
        
        assert isinstance(created_model, User)
        assert isinstance(created_model.id, int)
        
        read_model = await show(created_model.id, created_model)
        
        assert isinstance(read_model, User)
        assert isinstance(read_model.id, int)
        
        read_model = await get_by_creds(creds)
        
        assert isinstance(read_model, User)
        assert isinstance(read_model.id, int)
        
        try:
            creds.password = "wrong_password"
            await get_by_creds(creds)
            assert False
        except InvalidCredentials:
            assert True
        
        update_data = UserBaseFactory.build().model_dump(include={"name", "email"})
        update_data = UserProps(id=created_model.id, **update_data)
        
        updated_model = await update(read_model.id, update_data, created_model)
        assert isinstance(updated_model, User)
        assert updated_model.name == update_data.name
        assert updated_model.email == update_data.email
        
        assert await delete(updated_model.id, created_model)
        
        try:
            await show(created_model.id, created_model)
            assert False
        except NoResultFound:
            assert True
        
@pytest.mark.asyncio    
async def test_users_list():
    async with db():
        factory = UserRegisterFactory()
        created_models: list[User] = []
        
        admin = factory.build()
        admin = await create(admin)
        admin.role = Role.ADMIN
        
        create_models = [factory.build() for _ in range(10)]
        for model in create_models:
            m = await create(model)
            created_models.append(m)
            
        created_ids = [m.id for m in created_models]
        
        filter = UserFilter(ids=created_ids)
        pagination = PageRequest(page=1, per_page=len(create_models))
        request = UsersRequest(filters=filter, pagination=pagination)
        
        data_list = await list(request, created_models[0])
        assert len(data_list.data) == 1
        
        data_list = await list(request, admin)
        assert len(data_list.data) == len(create_models)
        
# @pytest.mark.asyncio
# async def test_users_list_action():
    


# PYTHONPATH=/code pytest /code/app/tests/test_user.py