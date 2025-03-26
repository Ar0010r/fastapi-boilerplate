from injector import inject
from app.business.command import CreateCommand
from app.business.schema.user import UserRegister
from app.business.schema.user import User, UserRegister
from app.business.service.user import UserService
from app.domain.model.user import User as UserEntity
from app.domain.repository.user import UserReader


class CreateUser(CreateCommand[UserRegister, User, UserEntity]):
    return_model = User
    
    @inject
    def __init__(self, service: UserService, reader: UserReader):
        self.service = service
        self.reader = reader