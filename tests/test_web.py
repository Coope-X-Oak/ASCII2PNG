import unittest
import json
import os
from web_app import app

class TestWebApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_generate_api_success(self):
        payload = {
            "text": "+---+\n| A |\n+---+",
            "width": 1080,
            "theme": "light"
        }
        response = self.client.post('/generate', 
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('image_url', data)
        self.assertIn('filename', data)

    def test_generate_api_empty_text(self):
        payload = {
            "text": "   ",
            "width": 1080
        }
        response = self.client.post('/generate', 
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
