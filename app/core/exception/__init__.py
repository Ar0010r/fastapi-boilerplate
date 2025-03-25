from fastapi import Request, status, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.http.routes import ResponseMetadata, ResponseSchema


def add(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(InvalidCredentials, invalid_credentials_exception_handler)
    app.add_exception_handler(InvalidToken, invalid_token_exception_handler)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_response = {}

    for error in errors:
        field = error["loc"][1]
        error_type = error["type"]
        error_response[field] = [error_type]
    
    dto = ResponseSchema(
        data=None,
        meta=ResponseMetadata(errors=error_response, message="validation error")
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(dto),
    )
    
class InvalidCredentials(Exception):
    def __init__(self, message: str = "Invalid credentials provided"):
        self.message = message
        super().__init__(self.message)
        
class InvalidToken(Exception):
    def __init__(self, message: str = "Invalid auth provided"):
        self.message = message
        super().__init__(self.message)
        
async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentials):
    dto = ResponseSchema(
        data=None,
        meta=ResponseMetadata(errors={"credentials": [exc.message]}, message="Invalid credentials")
    )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(dto),
    )
    
async def invalid_token_exception_handler(request: Request, exc: InvalidToken):
    dto = ResponseSchema(
        data=None,
        meta=ResponseMetadata(errors={"auth": [exc.message]}, message="Invalid auth")
    )

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(dto),
    )