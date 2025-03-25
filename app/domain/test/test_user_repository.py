import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.core import Role
from app.core.model import PageRequest
from app.domain.repository.user import UserEraser, UserReader, UserScope, UserWriter
from app.domain.model.user import User, UserFactory, UserFilter
        
@pytest.mark.asyncio
async def test_user_repositories_crud(session: AsyncSession):
    # factory = UserFactory()
    writer = UserWriter(session)
    reader = UserReader(session)
    eraser = UserEraser(session)

    create_data = UserFactory.build()
    id = await writer.create(create_data)
    created_product = await reader.find(id)

    assert isinstance(created_product, User)
    assert created_product.name == create_data.name
    assert created_product.email == create_data.email
    
    created_product.name = UserFactory.build().name
    assert await writer.update(created_product)
    
    updated_product = await reader.find(id)
    assert updated_product.name == created_product.name
    
    update_data = UserFactory.build()
    update_data = {"name": update_data.name, "email": update_data.email}
    rows_affected = await writer.modify(id, update_data)
    updated_product = await reader.find(id)
    
    assert rows_affected == 1
    assert updated_product.name == update_data["name"]
    assert updated_product.email == update_data["email"]
    
    rows_affected = await eraser.delete(id)
    assert rows_affected == 1

    await session.rollback()
    

@pytest.mark.asyncio    
async def test_users_list(session: AsyncSession):
    # factory = UserFactory()
    writer = UserWriter(session)
    reader = UserReader(session)
    created_models: list[User] = []
    
    admin_resolver = UserFactory.build()
    admin_resolver.role = Role.ADMIN
    await writer.create(admin_resolver)
    
    create_models = [UserFactory.build() for _ in range(10)]
    for model in create_models:
        id = await writer.create(model)
        m = await reader.find(id)
        created_models.append(m)
        
    created_ids = [m.id for m in created_models]
    random_email = create_models[0].email
    
    filter = UserFilter(ids=created_ids, )
    pagination = PageRequest(page=1, per_page=len(create_models))
    
    admin_scope = UserScope().get(admin_resolver)
    
    data_list = await reader.set_scope(admin_scope).filter(filter).paginate(pagination)
    assert data_list.count() == len(create_models)
    
    filter.email = random_email
    data_list = await reader.set_scope(admin_scope).filter(filter).paginate(pagination)
    assert data_list.count() == 1
    
    regular_scope = UserScope().get(create_models[0])
    data_list = await reader.set_scope(regular_scope).filter(filter).paginate(pagination)
    assert data_list.count() == 1
    
    filter.email = create_models[0].email
    data_list = await reader.set_scope(admin_scope).filter(filter).paginate(pagination)
    assert data_list.count() == 1
    
    await session.rollback()
    
    

# async def test_update_product(session: AsyncSession):
#     repository = UserWriter(session)
#     service = UserService(repository)
#     # Arrange
    
#     product_data = UserBase(name="Test User", price=100, description="Test Description")
#     id = await service.create(product_data)
    
#     product_data = UserBase(name="Updated User", price=19.99)
#     existing_product = User(id=1, name="Test User", price=10.99)

#     # Act
#     updated_product = service.update_product(existing_product, product_data)

#     # Assert
#     assert isinstance(updated_product, User)
#     assert updated_product.id == 1
#     assert updated_product.name == "Updated User"
#     assert updated_product.price == 19.99
    
#     session.rollback()

# def test_delete_product():
#     session.begin
#     repository = UserRepository(session)
#     service = UserService(repository)
#     # Arrange
#     existing_product = User(id=1, name="Test User", price=10.99)

#     # Act
#     service.delete_product(existing_product)
    
#     session.rollback()

#     # Assert
#     # Add assertions to check if the product is deleted successfully

# def test_get_product():
#     session.begin
#     repository = UserRepository(session)
#     service = UserService(repository)
#     # Arrange
#     existing_product = User(id=1, name="Test User", price=10.99)

#     # Act
#     retrieved_product = service.get_product(existing_product.id)

#     # Assert
#     assert isinstance(retrieved_product, User)
#     assert retrieved_product.id == 1
#     assert retrieved_product.name == "Test User"
#     assert retrieved_product.price == 10.99
    
#     session.rollback()


# PYTHONPATH=/code pytest /code/app/tests/test_product.py

