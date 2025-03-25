from injector import Injector
from app.business.schema import Product, ProductBase, ProductCreate, ProductInit, ProductProps, User
from app.business.schema.product import ProductRequest
from app.business.service.product import ProductService
from app.core.model import DataList
from app.domain.repository.product import ProductEraser, ProductReader, ProductScope

injector = Injector()
service = injector.get(ProductService)
reader = injector.get(ProductReader)
eraser = injector.get(ProductEraser)
scope = injector.get(ProductScope)

async def create(model: ProductInit, resolver: User) -> Product:
    dto = ProductCreate(**model.model_dump(), user_id=resolver.id)
    id = await service.create(dto)
    
    return await show(id, resolver)

async def update(id:int, model: ProductProps, resolver: User) -> Product:
    original = await show(id, resolver)
    await service.edit(original, model)
    
    return await show(id, resolver)

async def show(id: int, resolver: User) -> Product:
    data_scope = scope.get(resolver)
    reader.set_scope(data_scope).filter_id(id)
    model = await reader.first_or_fail()
    
    return Product.model_validate(model)

async def delete(id: int, resolver: User) -> bool:
    model = await show(id, resolver)
    result = await eraser.delete(model)
    
    return result > 0

async def list(r: ProductRequest, resolver: User) -> DataList[Product]:
    data_scope = scope.get(resolver)
    reader.set_scope(data_scope)
    reader.filter(r.filters)
    reader.order_by(r.order_by)
    data =  await reader.paginate(r.pagination)
    
    records = [Product.model_validate(m) for m in data.data]
    
    return DataList[Product](data=records, rows=data.rows)