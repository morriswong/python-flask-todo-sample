import unittest
import datetime
from server import app

##### UNIT TEST ######
class FlaskApiTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.app.get('/starred', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_search(self):
        response = self.app.post(
            '/searchResult',
            data=dict(
                search = 'search', 
                query = 'test string'
            ),follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_add_get(self):
        response = self.app.get('/add', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_post(self):
        response = self.app.post('/add',
            data=dict(title ="title", content="content"),
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
  unittest.main()