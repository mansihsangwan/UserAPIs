# Python
import unittest
import json
from app import create_app

class TestAPIs(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_create_user(self):
        # Positive test
        response = self.app.post('/users', data=json.dumps({'username': 'test121', 'email': 'test121@test.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Negative test: missing username
        response = self.app.post('/users', data=json.dumps({'email': 'test@test.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        # Positive test
        response = self.app.get('/users/1')
        self.assertEqual(response.status_code, 200)

        # Negative test: user not found
        response = self.app.get('/users/9999')
        self.assertEqual(response.status_code, 404)

    def test_run_command(self):
        # Positive test
        response = self.app.post('/run', data={'command': 'echo hello'})
        self.assertEqual(response.status_code, 200)

        # Negative test: missing command
        response = self.app.post('/run', data={})
        self.assertEqual(response.status_code, 400)

    def test_complex_method(self):
        # Positive test
        response = self.app.get('/complex')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)