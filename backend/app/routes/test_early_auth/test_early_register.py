# test_auth.py

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json

# Import the Blueprint under test
from app.routes.auth import auth_bp

@pytest.fixture
def client():
    """
    Fixture to create a Flask test client with the auth blueprint registered.
    """
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestRegister:
    """
    Unit tests for the 'register' function in app/routes/auth.py.
    """

    # -------------------- HAPPY PATHS --------------------

    @pytest.mark.happy_path
    def test_register_successful(self, client):
        """
        Test successful registration with valid username, email, and password.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword',
            'lang': 'en'
        }
        with patch('app.routes.auth.User.find_by_username', return_value=None), \
             patch('app.routes.auth.User.find_by_email', return_value=None), \
             patch('app.routes.auth.User.create_user', return_value=123), \
             patch('app.routes.auth.get_message', return_value='Registration successful!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 201
            resp_json = response.get_json()
            assert resp_json['success'] is True
            assert resp_json['message'] == 'Registration successful!'

    @pytest.mark.happy_path
    def test_register_successful_with_default_lang(self, client):
        """
        Test registration when 'lang' is not provided (should default to 'en').
        """
        data = {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.User.find_by_username', return_value=None), \
             patch('app.routes.auth.User.find_by_email', return_value=None), \
             patch('app.routes.auth.User.create_user', return_value=456), \
             patch('app.routes.auth.get_message', return_value='Registration successful!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 201
            resp_json = response.get_json()
            assert resp_json['success'] is True
            assert resp_json['message'] == 'Registration successful!'

    # -------------------- EDGE CASES --------------------

    @pytest.mark.edge_case
    def test_register_missing_username(self, client):
        """
        Test registration fails when username is missing.
        """
        data = {
            'email': 'test@example.com',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_missing_email(self, client):
        """
        Test registration fails when email is missing.
        """
        data = {
            'username': 'testuser',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_missing_password(self, client):
        """
        Test registration fails when password is missing.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_blank_username(self, client):
        """
        Test registration fails when username is blank or only whitespace.
        """
        data = {
            'username': '   ',
            'email': 'test@example.com',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_blank_email(self, client):
        """
        Test registration fails when email is blank or only whitespace.
        """
        data = {
            'username': 'testuser',
            'email': '   ',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_blank_password(self, client):
        """
        Test registration fails when password is blank.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': ''
        }
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_existing_username(self, client):
        """
        Test registration fails when username already exists.
        """
        data = {
            'username': 'existinguser',
            'email': 'newemail@example.com',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.User.find_by_username', return_value=MagicMock()), \
             patch('app.routes.auth.get_message', return_value='Username or email already exists!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 409
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Username or email already exists!'

    @pytest.mark.edge_case
    def test_register_existing_email(self, client):
        """
        Test registration fails when email already exists.
        """
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.User.find_by_username', return_value=None), \
             patch('app.routes.auth.User.find_by_email', return_value=MagicMock()), \
             patch('app.routes.auth.get_message', return_value='Username or email already exists!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 409
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Username or email already exists!'

    @pytest.mark.edge_case
    def test_register_create_user_failure(self, client):
        """
        Test registration fails with 500 if user creation fails (create_user returns None/False).
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword'
        }
        with patch('app.routes.auth.User.find_by_username', return_value=None), \
             patch('app.routes.auth.User.find_by_email', return_value=None), \
             patch('app.routes.auth.User.create_user', return_value=None), \
             patch('app.routes.auth.get_message', return_value='Registration failed!'):
            response = client.post('/api/register', json=data)
            assert response.status_code == 500
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Registration failed!'

    @pytest.mark.edge_case
    def test_register_non_json_payload(self, client):
        """
        Test registration fails gracefully if request data is not JSON.
        """
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', data="notjson", content_type='text/plain')
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'

    @pytest.mark.edge_case
    def test_register_empty_json(self, client):
        """
        Test registration fails when empty JSON is sent.
        """
        with patch('app.routes.auth.get_message', return_value='Missing fields!'):
            response = client.post('/api/register', json={})
            assert response.status_code == 400
            resp_json = response.get_json()
            assert resp_json['success'] is False
            assert resp_json['message'] == 'Missing fields!'