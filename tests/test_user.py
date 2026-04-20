from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get('/api/v1/user', params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]


def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get('/api/v1/user', params={'email': 'ghost@example.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    payload = {
        'name': 'Sergey Sergeev',
        'email': 's.s.sergeev@mail.com'
    }
    response = client.post('/api/v1/user', json=payload)
    assert response.status_code == 201
    assert response.json() == 3

    created_user = client.get('/api/v1/user', params={'email': payload['email']})
    assert created_user.status_code == 200
    assert created_user.json() == {
        'id': 3,
        'name': payload['name'],
        'email': payload['email']
    }


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    payload = {
        'name': 'Duplicate User',
        'email': users[0]['email']
    }
    response = client.post('/api/v1/user', json=payload)
    assert response.status_code == 409
    assert response.json() == {'detail': 'User with this email already exists'}


def test_delete_user():
    '''Удаление пользователя'''
    email = 's.s.sergeev@mail.com'
    response = client.delete('/api/v1/user', params={'email': email})
    assert response.status_code == 204
    assert response.text == ''

    deleted_user = client.get('/api/v1/user', params={'email': email})
    assert deleted_user.status_code == 404
    assert deleted_user.json() == {'detail': 'User not found'}
