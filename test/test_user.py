from ..main import app
import pytest
from fastapi.testclient import TestClient
from fastapi import status
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


def test_create_user_with_out_roles():
    user_1 = {'username': 'diego1', 'password': '123456',
              'tel': 000000000, 'email': 'diego@gmail1.com'}
    response = client.post('/user/create', json=user_1)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_user_with_roles():
    response_role = client.post(
        "/role/create/", json={'name': 'roltest', 'disabled': False})
    id_role = response_role.json()['id']
    user_1 = {'username': 'diegoconrol', 'password': '123456',
              'tel': 000000000, 'email': 'diegoconrol@gmail1.com', 'roles': [id_role]}
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


def test_update_user(setUp: setUp):
    header = setUp
    user_prueba = {'username': 'prueba', 'password': '123456',
                   'tel': 000000000, 'email': 'prueba@gmail.com'}
    response = client.post('/user/create', json=user_prueba)
    id_user = str(response.json()['id'])
    response_update = client.patch('/user/'+id_user, json={'username': 'pruebaedit', 'password': '123456',
                                                           'tel': 2222, 'email': 'pruebaedit@gmail1.com'}, headers=header)
    assert response_update.status_code == status.HTTP_200_OK


def test_delete_user(setUp: setUp):
    header = setUp
    user_prueba = {'username': 'prueba', 'password': '123456',
                   'tel': 000000000, 'email': 'prueba@gmail.com'}
    response = client.post('/user/create', json=user_prueba)
    id_user = response.json()['id']
    response_delete = client.delete(
        '/user/delete', params={'user_id': id_user}, headers=header)
    assert response_delete.status_code == status.HTTP_200_OK


def test_delete_user_with_roles_and_address(setUp: setUp):
    header = setUp
    user_prueba = {
        "username": "string",
        "password": "string",
        "name": "string",
        "surname": "string",
        "tel": 0,
        "email": "string",
        "created": "2023-08-06T21:52:26.915211",
        "disabled": False,
        "roles": [
            1
        ],
        "addresses": {
            "street": "string11",
            "province": "string",
            "city": "string",
            "postal_code": "string",
            "others": "string"
        }
    }
    response = client.post('/user/create', json=user_prueba)
    id_user = response.json()['id']
    response_delete = client.delete(
        '/user/delete', params={'user_id': id_user}, headers=header)
    assert response_delete.status_code == status.HTTP_200_OK


def test_get_user(setUp: setUp):
    header = setUp
    response = client.get('/user/1', headers=header)
    assert response.status_code == status.HTTP_200_OK


def test_get_users(setUp: setUp):
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
    assert response.status_code == status.HTTP_200_OK

# TODO TEST ACTUALIZAR ROLES DE USUARIOS

# def drop():
#     from config.database import engine
#     from db.models.base import Base
#     Base.metadata.drop_all(bind=engine)
