import json
import unittest
from uuid import uuid4

from fastapi.testclient import TestClient
from werkzeug.security import generate_password_hash

from src.basecore.error_handler import NOT_FOUND_ERROR_MESSAGE
from src.db.db_config import get_session
from src.main import app
from src.task.models import Task
from src.user.models import User
from src.user.utils import create_token


class TestTaskBase(unittest.TestCase):
    # Expected attributes:

    TASK_ID = 0
    USER_ID = 0
    CLIENT = TestClient(app)
    TASK_POST_DATA = {
        "question": ["Could you repeate please"],
        "answer": ["повторите пожалуйста", "можете ли вы повторить"],
        "type": 2
    }

    TASK_UPDATE_DATA = {
        "question": ["New question"],
        "answer": ["ответ1", "ответ2"],
    }

    TASK_CHECK_DATA = {'answer': TASK_POST_DATA["answer"][0]}

    @property
    def session(self):
        return get_session()

    def setUp(self):
        """Run before every test to prepare a database"""

        with get_session() as session:
            task_obj = Task(
                type=2,
                question=["Could you repeate please"],
                answer=["Повторите пожалуйста", "Можите ли вы повторить"]
            )
            session.add(task_obj)
            session.commit()
            session.refresh(task_obj)
            self.TASK_ID = str(task_obj.id)

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
            session.query(Task).delete()
            session.query(User).delete()
            session.commit()


class TestTaskAPIOk(TestTaskBase):

    def test_task_read(self):

        response = self.CLIENT.get('/task/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(type(result['data']), list)
        self.assertEqual(len(result['data']), 1)

    def test_task_read_if_empty(self):

        with get_session() as session:
            session.query(Task).delete()
            session.commit()

        response = self.CLIENT.get('/task/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(type(result['data']), list)
        self.assertEqual(len(result['data']), 0)

    def test_task_read_by_id(self):

        response = self.CLIENT.get(f'/task/task/{self.TASK_ID}/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(result['data']['id'], self.TASK_ID)

    def test_task_create(self):

        self.assertEqual(len(self.session.query(Task).all()), 1)

        response = self.CLIENT.post('/task/', json=self.TASK_POST_DATA)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(self.session.query(Task).all()), 2)

    def test_task_update(self):

        response = self.CLIENT.put(f'/task/task/{self.TASK_ID}/', json=self.TASK_UPDATE_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertEqual(result['data']['id'], self.TASK_ID)
        self.assertEqual(result['data']['question'], self.TASK_UPDATE_DATA['question'])
        self.assertEqual(result['data']['answer'], self.TASK_UPDATE_DATA['answer'])

    def test_task_delete(self):

        self.assertEqual(len(self.session.query(Task).all()), 1)

        response = self.CLIENT.delete(f'/task/task/{self.TASK_ID}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.session.query(Task).all()), 0)

    def test_task_get_random(self):

        response = self.CLIENT.get('/task/get_random/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertIn(result['data']['id'], [str(task.id) for task in self.session.query(Task).all()])

    def test_task_get_random_if_empty(self):

        with get_session() as session:
            session.query(Task).delete()
            session.commit()

        response = self.CLIENT.get('/task/get_random/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')
        self.assertFalse(result['data'])

    def test_task_check(self):

        response = self.CLIENT.post(f'/task/check_task/{self.TASK_ID}/', json=self.TASK_CHECK_DATA, headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)
        print(self.TASK_CHECK_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Success')

    def test_task_check_if_wrong_answer(self):

        response = self.CLIENT.post(f'/task/check_task/{self.TASK_ID}/', json={'answer': 'wrong'}, headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Try again')


class TestTaskAPIBad(TestTaskBase):

    def test_task_read_by_id_if_doesnt_exist(self):

        response = self.CLIENT.get(f'/task/task/{uuid4()}')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn(NOT_FOUND_ERROR_MESSAGE, result['message'])

    def test_task_create_if_empty_post_data(self):

        self.assertEqual(len(self.session.query(Task).all()), 1)

        response = self.CLIENT.post('/task/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Expecting value', result['message'])
        self.assertEqual(len(self.session.query(Task).all()), 1)

    def test_task_update_if_doesnt_exist(self):

        response = self.CLIENT.put(f'/task/task/{uuid4()}/', json=self.TASK_UPDATE_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn(NOT_FOUND_ERROR_MESSAGE, result['message'])

    def test_task_update_if_empty_body(self):

        response = self.CLIENT.put(f'/task/task/{self.TASK_ID}/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Expecting value', result['message'])

    def test_task_delete_if_doesnt_exist(self):

        self.assertEqual(len(self.session.query(Task).all()), 1)

        response = self.CLIENT.delete(f'/task/task/{uuid4()}/')
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn(NOT_FOUND_ERROR_MESSAGE, result['message'])
        self.assertEqual(len(self.session.query(Task).all()), 1)

    def test_task_check_if_not_authorized(self):

        response = self.CLIENT.post(f'/task/check_task/{self.TASK_ID}/', json=self.TASK_CHECK_DATA)
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 403)
        self.assertIn('Token is missing', result['message'])

    def test_task_check_if_doesnt_exist(self):

        response = self.CLIENT.post(f'/task/check_task/{uuid4()}/', json=self.TASK_CHECK_DATA, headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn(NOT_FOUND_ERROR_MESSAGE, result['message'])

    def test_task_check_if_empty_answer(self):

        response = self.CLIENT.post(f'/task/check_task/{self.TASK_ID}/', headers={
            'Authorization': create_token(user_id=self.USER_ID, time_delta_seconds=200)})
        result = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Expecting value', result['message'])
