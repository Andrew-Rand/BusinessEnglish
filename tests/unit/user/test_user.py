import json
import unittest
from copy import deepcopy

from starlette.testclient import TestClient
from werkzeug.security import generate_password_hash

from src.basecore.error_handler import NOT_FOUND_ERROR_MESSAGE
from src.db.db_config import get_session
from src.main import app
from src.user.models import User
from src.user.utils import create_token


class TestUserBase(unittest.TestCase):
    # Expected attributes:

    USER_ID = 0
    USER_SIGNUP_DATA = {
        "username": "Andrew",
        "email": "andrew@gmail.com",
        "password": "Abc123%%%"
    }
    USER_LOGIN_DATA = {
        "email": 'andr@gmail.com',
        "password": "Abc123%%%"
    }
    USER_UPDATE_DATA = {
        "username": "new_name",
        "email": 'new_email@gmail.com'
    }
    USER_CHANGE_PASSWORD_DATA = {
        "password": "Abc123%%%",
        "new_password": "Abc12345%%%",
        "new_password_repeated": "Abc12345%%%"
    }
    CLIENT = TestClient(app)
    EXPIRED_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjlhN2ZkMmZmLWQ5OTItNGE5ZS05NWYwLTU1MjY4ZGNmYmI0MSI" \
                    "sImV4cCI6MTY1NTExOTIyNSwiaWF0IjoxNjU1MTE4MDI1fQ.KaJi3r9496aIeElF07ByOU9hSKq3hPQLOqJ8vRdF5HE"

    @property
    def session(self):
        return get_session()

    def setUp(self):
        """Run before every test to prepare a database"""

        with get_session() as session:
            user_obj = User(
                username='Andrew',
                email='andr@gmail.com',
                password=generate_password_hash(password='Abc123%%%', method='sha256')
            )
            session.add(user_obj)
            session.commit()
            session.refresh(user_obj)
            self.USER_ID = str(user_obj.id)

    def tearDown(self):
        """Run after each tests in this class"""

        # rm all test data from db
        with get_session() as session:
            session.query(User).delete()
            session.commit()


class TestUserAPIOk(TestUserBase):

    def test_user_read(self):

        response = self.CLIENT.get('/user/', headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(type(result['data']), list)
        self.assertEqual(len(result['data']), 1)

    def test_user_read_by_id(self):

        response = self.CLIENT.get('/user/user/', headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(result['data']['id'], self.USER_ID)

    def test_user_update(self):

        response = self.CLIENT.put('/user/user/', json=self.USER_UPDATE_DATA, headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(result['data']['id'], self.USER_ID)
        self.assertEqual(result['data']['username'], self.USER_UPDATE_DATA['username'])
        self.assertEqual(result['data']['email'], self.USER_UPDATE_DATA['email'])

    def test_user_change_password(self):

        response = self.CLIENT.post('/user/change_password/', json=self.USER_CHANGE_PASSWORD_DATA, headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(result['data'], None)

    def test_user_signup(self):

        response = self.CLIENT.post('/user/signup/', json=self.USER_SIGNUP_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(result['data'], None)

    def test_user_login(self):
        response = self.CLIENT.post('/user/login/', json=self.USER_LOGIN_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertIn('access_token', result['data'].keys())
        self.assertIn('refresh_token', result['data'].keys())

    def test_user_refresh(self):
        response = self.CLIENT.post('/user/refresh/',
                                    json={"refresh_token": create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertIn('access_token', result['data'].keys())
        self.assertIn('refresh_token', result['data'].keys())


class TestUserAPIBad(TestUserBase):

    def test_user_read_if_not_authorized(self):

        response = self.CLIENT.get('/user/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', result['message'])

    def test_user_read_if_incorrect_token(self):

        response = self.CLIENT.get('/user/', headers={'Authorization': 'token'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid token. Please log in again', result['message'])

    def test_user_read_if_empty(self):

        with get_session() as session:
            session.query(User).delete()
            session.commit()

        response = self.CLIENT.get('/user/', headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn('User is not found', result['message'])

    def test_user_read_by_id_if_not_authorized(self):

        response = self.CLIENT.get('/user/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', result['message'])

    def test_user_read_by_id_if_incorrect_token(self):

        response = self.CLIENT.get('/user/', headers={'Authorization': 'token'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid token. Please log in again', result['message'])

    def test_user_read_by_id_if_expired_token(self):

        response = self.CLIENT.get('/user/', headers={'Authorization': self.EXPIRED_TOKEN})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Access token is expired, go to the refresh endpoint', result['message'])

    def test_user_read_by_id_if_doesnt_exist(self):

        with get_session() as session:
            session.query(User).delete()
            session.commit()

        response = self.CLIENT.get('/user/user/', headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn('User is not found', result['message'])

    def test_user_update_if_not_authorized(self):

        response = self.CLIENT.put('/user/user/', json=self.USER_UPDATE_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', result['message'])

    def test_user_update_if_incorrect_token(self):

        response = self.CLIENT.put('/user/user/', json=self.USER_UPDATE_DATA, headers={'Authorization': 'token'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid token. Please log in again', result['message'])

    def test_user_change_password_if_doesnt_exist(self):

        with get_session() as session:
            session.query(User).delete()
            session.commit()

        response = self.CLIENT.post('/user/change_password/', json=self.USER_CHANGE_PASSWORD_DATA, headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn('User is not found', result['message'])

    def test_user_change_password_if_not_authprized(self):

        response = self.CLIENT.post('/user/change_password/', json=self.USER_CHANGE_PASSWORD_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', result['message'])

    def test_user_change_password_if_incorrect_token(self):

        response = self.CLIENT.post('/user/change_password/', json=self.USER_CHANGE_PASSWORD_DATA,
                                    headers={'Authorization': 'token'})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid token. Please log in again', result['message'])

    def test_user_signup_if_empty_data(self):

        response = self.CLIENT.post('/user/signup/')

        self.assertEqual(response.status_code, 422)

    def test_user_signup_if_incorrect_request_values(self):

        incorrect_values = {
            "username": 24,
            "email": "email",
            "password": "1111"
        }

        for key in incorrect_values.keys():
            new_post_data = deepcopy(self.USER_SIGNUP_DATA)
            new_post_data[key] = incorrect_values[key]

            response = self.CLIENT.post('/user/signup/', json=new_post_data)

            self.assertEqual(response.status_code, 400)

    def test_user_login_if_wrong_creds(self):

        response = self.CLIENT.post('/user/login/', json=self.USER_SIGNUP_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn(NOT_FOUND_ERROR_MESSAGE, result['message'])

    def test_user_login_if_empty_request_data(self):

        response = self.CLIENT.post('/user/login/')

        self.assertEqual(response.status_code, 422)

    def test_user_refresh_if_empty_request_data(self):

        response = self.CLIENT.post('/user/refresh/')

        self.assertEqual(response.status_code, 422)

    def test_user_refresh_if_incorrect_token(self):
        response = self.CLIENT.post('/user/refresh/', json={"refresh_token": "token"})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid token. Please log in again', result['message'])

    def test_user_refresh_if_expired_token(self):
        response = self.CLIENT.post('/user/refresh/', json={"refresh_token": self.EXPIRED_TOKEN})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Refresh token is expired, go to the refresh endpoint', result['message'])
