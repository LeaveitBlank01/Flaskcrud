import unittest
from api import app 

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
    
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_get_people(self):
        response = self.app.get("/people")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.data.decode())

    def test_get_people_by_id(self):
        response = self.app.get("/people/2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jane" in response.data.decode())


if __name__ == "__main__":
    unittest.main()
