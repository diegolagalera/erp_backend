from ..main import app
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
client = TestClient(app)
# from config.database import engine
# from db.models.base import Base
# Base.metadata.drop_all(bind=engine)


# @pytest.fixture(scope="function")
# def user1():
#     return {'username': 'diego1', 'password': '123456',
#             'tel': 000000000, 'email': 'diego@gmail1.com'}


# @pytest.fixture(scope="function")
# def client() -> TestClient:
#     "start Client"
#     return TestClient(app)

@pytest.fixture
def setUp(client: TestClient):
    print('ooooooooooooooooooooooooooo')
    user_1 = {'username': 'admin', 'password': 'admin',
              'tel': 000000000, 'email': 'admin@gmail.com', 'roles': [1]}
    role = client.post(
        "/role/create/", json={'name': 'admin', 'disabled': False})
    user_insert = client.post('/user/create', json=user_1)
    # id = str(user_insert.json()['id'])
    login_user = {'username': 'admin', 'password': 'admin'}
    login = client.post('/auth/login', data=login_user)
    header = {'Authorization': 'Bearer ' + login.json()["access_token"]}
    yield header


# def test_createUser(client: TestClient):
def test_createUser():
    user_1 = {'username': 'diego1', 'password': '123456',
              'tel': 000000000, 'email': 'diego@gmail1.com'}
    response = client.post('/user/create', json=user_1)
    assert response.status_code == status.HTTP_201_CREATED


def test_login():
    login_user = {'username': 'diego1', 'password': '123456'}
    response = client.post('/auth/login', data=login_user)
    assert response.status_code == status.HTTP_200_OK


def test_error_in_login():
    login_user = {'username': 'fake', 'password': 'fake'}
    response = client.post('/auth/login', data=login_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_user(setUp: setUp):
    header = setUp
    response = client.get('/user/1', headers=header)
    assert response.status_code == status.HTTP_200_OK


def test_usersError(setUp: setUp):
    header = setUp
    data = {
        "params": [
            {
                "limit": 10,
                "offset": 0
            }
        ]
    }
    response = client.post('/user', json=data, headers=header)
    print(response)
    assert response.status_code == status.HTTP_200_OK

# DELETE / UPDATE

# client.drop_all()
# def test_createRole(setUp: setUp):
#     print('user')
#     header = setUp
#     print(header)
#     assert 'ok' == 'ok'
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


# def drop():
#     from config.database import engine
#     from db.models.base import Base
#     Base.metadata.drop_all(bind=engine)
