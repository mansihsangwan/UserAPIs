import unittest
import json
from flask import Flask
from app import create_app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config['TESTING'] = True
        self.client = app.test_client()
        # self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('username', response.json)
        self.assertIn('email', response.json)

    def test_get_user(self):
        # Assuming a user with ID 1 exists
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json)
        self.assertIn('email', response.json)

    def test_run_command(self):
        response = self.client.post('/run', data={'command': 'echo Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello', response.data.decode())

    def test_complex_method(self):
        response = self.client.get('/complex')
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.json)

    def test_buggy_endpoint(self):
        response = self.client.post('/buggy', json={'key': 'value'})
        self.assertEqual(response.status_code, 500)  # Expecting a server error due to the bug

    def test_unsafe_get_user(self):
        response = self.client.get('/unsafe_user/testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json)
        self.assertIn('email', response.json)

    def test_get_file(self):
        response = self.client.get('/files/testfile.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('file content', response.data.decode())

    def test_post_comment(self):
        response = self.client.post('/comment', json={'text': 'This is a comment'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Thanks for your comment:', response.data.decode())

    def test_buffer_overflow(self):
        response = self.client.post('/buffer', json={'input': 'A' * 101})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Input stored', response.json['message'])

    def test_unhandled_exception(self):
        response = self.client.get('/exception')
        self.assertEqual(response.status_code, 500)  # Expecting a server error due to the exception

    def test_get_date(self):
        response = self.client.get('/date')
        self.assertEqual(response.status_code, 200)
        self.assertIn('date', response.json)

    def test_get_length(self):
        response = self.client.get('/length/teststring')
        self.assertEqual(response.status_code, 200)
        self.assertIn('length', response.json)

    def test_unsafe_method(self):
        response = self.client.get('/unsafe/testuser/testfile.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('file content', response.data.decode())

    def test_process_people(self):
        people = [
            {'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'name': 'Bob', 'age': 17, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 25, 'city': 'Chicago'}
        ]
        expected_results = [
            {'name': 'Alice', 'age_group': 'adult', 'city_group': 'NY', 'char_type': 'uppercase', 'status': 'NY Adult'},
            {'name': 'Bob', 'age_group': 'minor', 'city_group': 'LA', 'char_type': 'uppercase', 'status': 'Minor or Unknown'},
            {'name': 'Charlie', 'age_group': 'adult', 'city_group': 'Other', 'char_type': 'consonant', 'status': 'Other Adult'}
        ]
        results = process_people(people)
        self.assertEqual(results, expected_results)

if __name__ == '__main__':
    unittest.main()