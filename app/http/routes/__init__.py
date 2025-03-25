from typing import Generic, TypeVar, Any, Optional, List
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_responseschema import AbstractResponseSchema, SchemaAPIRoute


# Build your "Response Schema"
class ResponseMetadata(BaseModel):
    errors: dict = {}
    message: Optional[str]


T = TypeVar("T")


class ResponseSchema(AbstractResponseSchema[T], Generic[T]):
    data: T
    meta: ResponseMetadata

    @classmethod
    def from_exception(cls, reason, status_code, message: str = "Error", **others):
        
        return cls(
            data=reason,
            meta=ResponseMetadata(errors={}, message=message)
            # meta=ResponseMetadata(errors=reason, message=message)
        )

    @classmethod
    def from_api_route(
        cls, content: Any, status_code: int, description: Optional[str] = None, **others
    ):
        return cls(
            data=content,
            meta=ResponseMetadata(error=status_code >= 400, message=description)
        )


# Create an APIRoute
class Route(SchemaAPIRoute):
    response_schema = ResponseSchema