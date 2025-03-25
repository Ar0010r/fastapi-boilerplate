from app.business.schema.user import UserBaseFactory, UserProps, UserRegisterFactory
from app.core import jwt

update_route = "user/{id}"
delete_route = "user/{id}"
show_route = "user/{id}"
register_route = "register"

def test_user_crud(test_client):
    create_data = UserRegisterFactory.build()
    update_data = UserBaseFactory.build().model_dump(include={"name", "email"})
    
    create_response = test_client.post(
        register_route,
        json=create_data.model_dump()
    )
    
    token = create_response.json()['data']
    headers = {"Authorization": f"Bearer {token}"}
    
    assert create_response.status_code == 200
    assert isinstance(token, str)
    
    id = int(jwt.decode(token).sub)
    
    assert isinstance(id, int)
    assert id > 0
    
    update_data = UserProps(id=id, **update_data)
    test_client.put(
        update_route.format(id=id),
        headers=headers,
        json=update_data.model_dump(exclude_unset=True)
    )
    
    response = test_client.get(show_route.format(id=id), headers=headers)
    response_data = response.json()["data"]
    
    assert response.status_code == 200
    assert response_data["name"] == update_data.name
    assert response_data["email"] == update_data.email
    
    response = test_client.delete(delete_route.format(id=id), headers=headers)
    assert response.status_code == 200
    
    
def test_auth_guard(test_client):
    id = 0
    any_data = {}
    
    response = test_client.get(show_route.format(id=id))
    assert response.status_code == 401
    
    response = test_client.put(update_route.format(id=id), json=any_data)
    assert response.status_code == 401
    
    response = test_client.delete(delete_route.format(id=id))
    assert response.status_code == 401
    
    
    
    
    
    
    
    
 # response = test_client.post(
    #     create_route,
    #     json=create_data.model_dump()
    # )
    
    # response_data = response.json()["data"]

    # assert response.status_code == 200
    # assert isinstance(response_data['id'], int)
    # assert response_data["name"] == create_data.name
    # assert response_data["email"] == create_data.email