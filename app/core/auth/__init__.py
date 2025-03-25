from abc import ABC, abstractmethod
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Authenticable(ABC):
    @abstractmethod
    def get_claims(self) -> jwt.Claims:
        pass

def issue_token(model: Authenticable) -> str:
    claims = model.get_claims()
    
    return jwt.encode(claims)

def get_token(token: str = Depends(oauth2_scheme)) -> str:
   return token