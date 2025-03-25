import time 
from typing import Optional
import jwt
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

ALGO: str = "HS256"
EXP: int = 36000000

class Config(BaseSettings):
    secret: str = "secret"
    exp:Optional[int] = EXP
    
    model_config = SettingsConfigDict(env_file='/code/.env', case_sensitive=False, env_file_encoding='utf-8', extra='ignore' )

config = Config()

class Claims(BaseModel):
    sub: str
    exp: Optional[int] = None
    iat: Optional[int] = None
    
def encode(claims: Claims) -> str:
    secret = config.secret
    exp = config.exp
    timestamp = int(time.time())
    claims.exp = claims.exp or (timestamp + exp)
    claims.iat = claims.iat or timestamp
        
    payload = claims.model_dump()
    
    return jwt.encode(payload, secret, algorithm=ALGO)

def decode(token: str) -> Claims:
    secret = config.secret
    token = strip_bearer(token)
    payload = jwt.decode(token, secret, algorithms=[ALGO])
    
    return Claims(**payload)

def strip_bearer(token: str) -> str:
    return token.replace("Bearer ", "")


