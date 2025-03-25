from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bcrypt_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

class Bcrypt():
    @staticmethod
    def verify(plain, hashed) -> bool:
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def hash(value: str) -> str:
        return pwd_context.hash(value)
    
    @staticmethod
    def hash_once(value: str) -> str:
        if Bcrypt.is_hashed(value):
            return value
        
        return pwd_context.hash(value)
    
    @staticmethod
    def is_hashed(value: str) -> bool:
        return bool(re.match(bcrypt_regex, value))