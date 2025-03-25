from typing import Type
import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.business.schema.product import ProductFilter
from app.core import Role
from app.core.model import PageRequest
from app.domain.model.factory import ProductFactory
from app.domain.repository.product import ProductEraser, ProductReader, ProductScope, ProductWriter
from app.domain.model import Product
from app.domain.test.conftest import temp_user
        
@pytest.mark.asyncio
async def test_product_repositories_crud(session: AsyncSession):
    factory = ProductFactory()
    writer = ProductWriter(session)
    reader = ProductReader(session)
    eraser = ProductEraser(session)
    user = await temp_user(session)

    create_data = factory.build()
    create_data.user_id = user.id
    id = await writer.create(create_data)
    created_product = await reader.find(id)

    assert isinstance(created_product, Product)
    assert created_product.name == create_data.name
    assert created_product.price == create_data.price
    
    created_product.name = factory.build().name
    assert await writer.update(created_product)
    
    updated_product = await reader.find(id)
    assert updated_product.name == created_product.name
    
    update_data = factory.build()
    update_data = {"name": update_data.name, "price": update_data.price}
    rows_affected = await writer.modify(id, update_data)
    updated_product = await reader.find(id)
    
    assert rows_affected == 1
    assert updated_product.name == update_data["name"]
    assert updated_product.price == update_data["price"]
    
    rows_affected = await eraser.delete(id)
    assert rows_affected == 1

    await session.rollback()
    

@pytest.mark.asyncio    
async def test_products_list(session: AsyncSession):
    factory = ProductFactory()
    writer = ProductWriter(session)
    reader = ProductReader(session)
    eraser = ProductEraser(session)
    user = await temp_user(session)
    another_user = await temp_user(session)
    user.role = Role.ADMIN

    created_models: list[Product] = []
    
    create_data = [factory.build() for _ in range(10)]
    for model in create_data:
        model.user_id = user.id
        id = await writer.create(model)
        m = await reader.find(id)
        created_models.append(m)
        
    created_ids = [m.id for m in created_models]
    
    filter = ProductFilter(ids=created_ids)
    pagination = PageRequest(page=1, per_page=len(create_data))
    
    admin_scope = ProductScope().get(user)
    
    data_list = await reader.set_scope(admin_scope).filter(filter).paginate(pagination)
    assert len(data_list.data) == len(create_data)
    
    user.role = Role.REGULAR
    regular_scope = ProductScope().get(user)
    data_list = await reader.set_scope(regular_scope).filter(filter).paginate(pagination)
    assert len(data_list.data) == len(create_data)
    
    regular_scope = ProductScope().get(another_user)
    data_list = await reader.set_scope(regular_scope).filter(filter).paginate(pagination)
    assert len(data_list.data) == 0
    
    await session.rollback()

