

from app.business.schema.user import UserRegisterFactory
from app.core.model import Credentials


login_route = "login"
register_route = "register"
auth_user_route = "auth-user"

def test_auth(test_client):
    create_data = UserRegisterFactory.build()
    creds = Credentials(email=create_data.email, password=create_data.password)
    
    response = test_client.post(
        register_route,
        json=create_data.model_dump()
    )
    
    token = response.json()['data']
    
    assert response.status_code == 200
    assert isinstance(token, str)
    
    response = test_client.post(
        login_route,
        json=create_data.model_dump()
    )
    
    token = response.json()['data']
    
    assert response.status_code == 200
    assert isinstance(token, str)
    
    response = test_client.get(
        auth_user_route,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    id = token = response.json()['data']['id']
    
    assert isinstance(id, int)
    
    
