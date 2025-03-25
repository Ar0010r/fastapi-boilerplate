from fastapi import Depends
from app.business.service import BaseService
from app.domain.model import Product
from app.domain.repository.product import ProductWriter
from injector import inject

class ProductService(BaseService[Product]):
    
    @inject
    def __init__(self, repository: ProductWriter):
        self.model = Product
        self.repository = repository