from injector import Injector
from app.business.schema.user import User, UserBase, UserProps, UserRegister, UsersRequest
from app.core import auth, jwt
from app.core.hashing.bcrypt import Bcrypt
from app.core.model import DataList
from app.domain.model.user import User as UserModel, UserFilter
from app.business.service.user import UserService
from app.core.database.postgres import Credentials
from app.core.exception import InvalidCredentials, InvalidToken
from app.domain.repository.user import UserEraser, UserReader, UserScope

injector = Injector()
service = injector.get(UserService)
reader = injector.get(UserReader)
eraser = injector.get(UserEraser)
scope = injector.get(UserScope)

async def create(model: UserRegister) -> User:
    id = await service.create(model)
    model = await reader.find_or_fail(id)
    
    return User.model_validate(model)


async def update(id:int, model: UserProps, resolver: User) -> User:
    model.id = id
    await show(id, resolver)
    await service.modify(model)
    
    a =  await show(id, resolver)
    
    return a


async def show(id: int, resolver: User) -> User:
    data_scope = scope.get(resolver)
    reader.set_scope(data_scope).filter_id(id)
    model = await reader.first_or_fail()
    
    return User.model_validate(model)


async def delete(id: int, resolver: User) -> bool:
    model = await show(id, resolver)
    result = await eraser.delete(id)
    
    return result > 0


async def list(r: UsersRequest, resolver: User) -> DataList[User]:
    data_scope = scope.get(resolver)
    reader.set_scope(data_scope)
    reader.filter(r.filters)
    reader.order_by(r.order_by)
    data =  await reader.paginate(r.pagination)
    
    records = [User.model_validate(m) for m in data.data]
    
    return DataList[User](data=records, rows=data.rows)


async def get_by_creds(creds: Credentials) -> User:
    user = await reader.find_by_email(creds.email)
    exists = isinstance(user, UserModel)
    
    result = exists and Bcrypt.verify(creds.password, user.password)
    
    if not result:
        raise InvalidCredentials() 
    
    return User.model_validate(user)

async def get_by_token(token: str) -> User:
    
    try:
        id = jwt.decode(token).sub
        id = int(id)
    except (Exception) as e:
        raise InvalidToken() 
    
    user = await reader.find(id)
    
    if not user:
        raise InvalidToken() 
    
    return User.model_validate(user)