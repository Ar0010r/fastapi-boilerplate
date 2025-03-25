from typing import Type
import pytest

from app.business.action.auth import register, login
from app.business.action.user import get_by_token
from app.business.schema.user import User, UserRegisterFactory

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.postgres import db_creds
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from fastapi import FastAPI

from app.core.exception import InvalidCredentials, InvalidToken
from app.core.model import Credentials

SQLAlchemyMiddleware(app = FastAPI(), db_url = db_creds.get_pg_url())
        
# @pytest.mark.asyncio
# async def test_auth_actions(session: AsyncSession):
#     async with db():
#         create_data = UserRegisterFactory.build()
#         creds = Credentials(email=create_data.email, password=create_data.password)
#         token = await register(create_data)
        
#         assert isinstance(token, str)
#         token = await login(creds)
        
#         assert isinstance(token, str)
        
#         user = await get_by_token(token)
        
#         assert isinstance(user, User)
        
#         try:
#             await get_by_token("wrong_token")
#             assert False
#         except InvalidToken:
#             assert True
        
#         try:
#             creds.password = "wrong_password"
#             await login(creds)
#             assert False
#         except InvalidCredentials:
#             assert True
        
        
        
        


# PYTHONPATH=/code pytest /code/app/tests/test_user.py

