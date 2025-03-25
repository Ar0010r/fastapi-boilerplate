import time

import pytest

from app.business.schema import ProductInitFactory
from app.http.tests.conftest import temp_token

create_route = "product"
update_route = "product/{id}"
delete_route = "product/{id}"
show_route = "product/{id}"

@pytest.mark.asyncio
async def test_product_crud(test_client):
    token = await temp_token(test_client)
    headers = {"Authorization": f"Bearer {token}"}
    create_data = ProductInitFactory.build()
    update_data = ProductInitFactory.build()
    response = test_client.post(
        create_route,
        headers=headers,
        json=create_data.model_dump()
    )
    
    response_data = response.json()["data"]

    id = response_data["id"]
    assert isinstance(id, int)
    assert response.status_code == 200
    assert response_data["name"] == create_data.name
    assert response_data["price"] == create_data.price
    assert response_data["description"] == create_data.description
    
    response = test_client.put(
        update_route.format(id=id),
        headers=headers,
        json=update_data.model_dump()
    )
    
    response_data = response.json()["data"]
    
    assert response.status_code == 200
    assert response_data["name"] == update_data.name
    assert response_data["price"] == update_data.price
    assert response_data["description"] == update_data.description
    
    response = test_client.get(show_route.format(id=id), headers=headers,)
    response_data = response.json()["data"]
    
    assert response.status_code == 200
    assert response_data["name"] == update_data.name
    assert response_data["price"] == update_data.price
    assert response_data["description"] == update_data.description
    
def test_auth_guard(test_client):
    id = 0
    any_data = {}
    
    response = test_client.get(show_route.format(id=id))
    assert response.status_code == 401
    
    response = test_client.put(update_route.format(id=id), json=any_data)
    assert response.status_code == 401
    
    response = test_client.delete(delete_route.format(id=id))
    assert response.status_code == 401
    
    
    
    
    
    