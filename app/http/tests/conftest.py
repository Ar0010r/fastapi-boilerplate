import pytest
from fastapi.testclient import TestClient
from app.business.action import auth
from app.business.schema.user import UserRegisterFactory
from app.domain.repository.user import UserWriter
from app.main import app
from app.http.tests.test_auth_http import register_route
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as test_client:
        yield test_client

async def temp_token(client: TestClient) -> str:
    user = UserRegisterFactory().build()
    create_response = client.post(
        register_route,
        json=user.model_dump()
    )
    
    return create_response.json()['data'] 
    