import unittest
import json
from app import create_app

class TestAPIs(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_create_user(self):
        response = self.app.post('/users', data=json.dumps({'username': 'test1', 'email': 'test1@test.com'}), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_user(self):
        response = self.app.get('/users/199')
        self.assertEqual(response.status_code, 200)

    def test_run_command(self):
        response = self.app.post('/run', data={'command': 'echo hello'})
        self.assertEqual(response.status_code, 200)

    def test_complex_method(self):
        response = self.app.get('/complex')
        self.assertEqual(response.status_code, 200)

    # def test_buggy_endpoint(self):
    #     response = self.app.post('/buggy', data=json.dumps({'key': 'value'}), content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()