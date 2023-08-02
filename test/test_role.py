from ..main import app
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status

# client = TestClient(app)
# roleTest: {
#     'name': 'roleTest1',
#     'disabled': False
# }


# @pytest.fixture(scope="function")
# def client() -> TestClient:
#     "start Client"
#     return TestClient(app)


# @pytest.fixture
# def setUp(client: TestClient):
#     print('ooooooooooooooooooooooooooo')
#     user_1 = {'username': 'diego1', 'password': '123456',
#               'tel': 000000000, 'email': 'diego@gmail1.com'}
#     user_insert = client.post('/user/create', json=user_1)
#     # assert user_insert.status_code == status.HTTP_201_CREATED
#     login_user = {'username': 'diego1', 'password': '123456'}
   
#     login = client.post('/auth/login', data=login_user)
#     print('iiiiiiiiiiiiiiiiiiii')
#     print(user_insert)
#     print(login.json())
#     header = {'Authorization': 'Bearer ' + login.json()["access_token"]}
#     yield header
#     # yield user_insert


# def test_createRole(client: TestClient, setUp: setUp):
#     print('user')
#     print()
    # response = client.post(
    #     "/role/create/",
    #     # headers={"X-Token": "coneofsilence"},
    #     json={
    #         'name': 'roleTest1',
    #         'disabled': False
    #     }
    # )
    # assert response.status_code == 201
    # print(response.json())


# def test_getRole():
#     response = client.get('/role/1')
#     # assert response == {'pep': 'pp'}
#     print('ppppppppppppppppppppppppppp')
#     print(response)
#     print(response.json())
#     assert response.status_code == 200


# def test_drop_db():
#     from config.database import engine
#     from db.models.base import Base
#     Base.metadata.drop_all(bind=engine)
