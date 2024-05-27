import unittest
from api import app, auth  
from base64 import b64encode

class MyAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config["TESTING"] = True
        self.credentials = b64encode(b"admin:123456").decode('utf-8')
        self.auth_headers = {"Authorization": f"Basic {self.credentials}"}

    def test_index_page(self):
        with app.app_context():
            response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_get_people(self):
        with app.app_context():
            response = self.app.get("/people", headers=self.auth_headers) 
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.data.decode())

    def test_get_people_by_id(self):
        with app.app_context():
            response = self.app.get("/people/2", headers=self.auth_headers)  
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jane" in response.data.decode())

    def test_get_people_unauthorized(self):
        with app.app_context():
            response = self.app.get("/people") 
        self.assertEqual(response.status_code, 401) 

    def test_create_person(self):
        with app.app_context():
            response = self.app.post("/people", headers=self.auth_headers, json={"first_name": "Tanggol", "last_name": "Aso", "age": 30, "city": "New York"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Person created successfully", response.data.decode())

    def test_update_person(self):
        with app.app_context():
            response = self.app.put("/people/1", headers=self.auth_headers, json={"first_name": "Bob", "last_name": "Arum", "age": 35, "city": "Los Angeles"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person updated successfully", response.data.decode())

    def test_delete_person(self):
        with app.app_context():
            response = self.app.delete("/people/1", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person deleted successfully", response.data.decode())

    def test_search_people(self):
        with app.app_context():
            response = self.app.get("/people/search?query=John", headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)

    def test_search_people_no_query(self):
        with app.app_context():
            response = self.app.get("/people/search", headers=self.auth_headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()
