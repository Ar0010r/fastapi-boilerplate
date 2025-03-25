from polyfactory.factories import DataclassFactory

from app.domain.model import Product

class ProductFactory(DataclassFactory[Product]):
    __model__ = Product
    

