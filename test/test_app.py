import sys
import os
import unittest
import json

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('version', data)

    def test_info_endpoint(self):
        response = self.app.get('/info')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('app_name', data)
        self.assertIn('environment', data)
        self.assertIn('python_version', data)
        self.assertIn('timestamp', data)

    def test_get_notes(self):
        response = self.app.get('/api/notes')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('notes', data)
        self.assertIsInstance(data['notes'], list)

    def test_create_note(self):
        test_note = {
            'title': 'Test Note',
            'content': 'This is a test note created during unit testing.'
        }
        response = self.app.post('/api/notes',
                                data=json.dumps(test_note),
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('note', data)
        self.assertEqual(data['note']['title'], test_note['title'])
        self.assertEqual(data['note']['content'], test_note['content'])

if __name__ == '__main__':
    unittest.main()