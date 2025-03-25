from typing import Type
import pytest

from app.business.action.product import create, show, update, delete, list
from app.business.schema import Product, ProductBaseFactory, ProductInitFactory, ProductProps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from app.business.schema.product import ProductFilter, ProductRequest
from app.core.database.postgres import db_creds
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from fastapi import FastAPI

from app.core.model import PageRequest
from app.domain.test.conftest import temp_user

SQLAlchemyMiddleware(app = FastAPI(debug=True), db_url = db_creds.get_pg_url(), engine_args=db_creds.engine_args)
        
@pytest.mark.asyncio
async def test_product_actions():
    async with db():
        user = await temp_user(db.session)
        create_data = ProductInitFactory.build()
        created_model = await create(create_data, user)
        
        assert isinstance(created_model, Product)
        
        read_model = await show(created_model.id, user)
        
        assert isinstance(read_model, Product)
        
        update_data = ProductInitFactory.build().model_dump(include={"name", "price"})
        update_data = ProductProps(id=created_model.id, **update_data)
        
        updated_model = await update(read_model.id, update_data, user)
        assert isinstance(updated_model, Product)
        assert updated_model.name == update_data.name
        assert updated_model.price == update_data.price
        
        assert await delete(updated_model.id, user)
        
        try:
            await show(created_model.id, user)
            assert False
        except NoResultFound:
            assert True
            
@pytest.mark.asyncio    
async def test_products_list():
    async with db():
        user = await temp_user(db.session)
        factory = ProductInitFactory()
        created_models: list[Product] = []
        
        create_models = [factory.build() for _ in range(10)]
        for model in create_models:
            m = await create(model, user)
            created_models.append(m)
        
        created_ids = [m.id for m in created_models]
        
        filter = ProductFilter(ids=created_ids)
        pagination = PageRequest(page=1, per_page=len(create_models))
        request = ProductRequest(filters=filter, pagination=pagination)
        
        data_list = await list(request, user)
        assert data_list.count() == len(create_models)
        
        user2 = await temp_user(db.session)
        data_list = await list(request, user2)
        assert data_list.count() == 0
        
        request.filters.name = create_models[0].name
        data_list = await list(request, user)
        assert data_list.count() == 1
        


# PYTHONPATH=/code pytest /code/app/tests/test_product.py

