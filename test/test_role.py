from ..main import app
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException, status

client = TestClient(app)


@pytest.fixture
def setUp():
    user_1 = {'username': 'admin', 'password': 'admin',
              'tel': 000000000, 'email': 'admin@gmail.com', 'roles': [1]}
    client.post(
        "/role/create/", json={'name': 'admin', 'disabled': False})
    client.post('/user/create', json=user_1)
    login_user = {'username': 'admin', 'password': 'admin'}
    login = client.post('/auth/login', data=login_user)
    header = {'Authorization': 'Bearer ' + login.json()["access_token"]}
    yield header


def test_create_role():
    role = {'name': 'test'}
    response = client.post('/role/create', json=role)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_role(setUp: setUp):
    header = setUp
    role = {'name': 'test2'}
    response_create = client.post('/role/create', json=role)
    id_role = str(response_create.json()['id'])

    response_update = client.patch(
        '/role/'+id_role, json={'name': 'test2edit'}, headers=header)
    assert response_update.status_code == status.HTTP_200_OK


def test_get_role(setUp: setUp):
    header = setUp
    role = {'name': 'test3'}
    response_create = client.post('/role/create', json=role)
    role_id = str(response_create.json()['id'])
    response = client.get('/role/'+role_id, headers=header)
    assert response.status_code == status.HTTP_200_OK


def test_get_roles(setUp: setUp):
    header = setUp
    data = {
        "params": [
            {
                "limit": 10,
                "offset": 0
            }
        ]
    }
    role4 = {'name': 'test4'}
    role5 = {'name': 'test4'}
    client.post('/role/create', json=role4)
    client.post('/role/create', json=role5)
    response = client.post('/role', json=data, headers=header)
    assert response.status_code == status.HTTP_200_OK


def test_delete_role(setUp: setUp):
    header = setUp
    role_prueba = {'name': 'prueba'}
    response = client.post('/role/create', json=role_prueba)
    role_id = response.json()['id']
    response_delete = client.delete(
        '/role/delete', params={'role_id': role_id}, headers=header)
    assert response_delete.status_code == status.HTTP_200_OK


# def test_drop_db():
#     from config.database import engine
#     from db.models.base import Base
#     Base.metadata.drop_all(bind=engine)
