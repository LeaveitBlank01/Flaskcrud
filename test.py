import unittest
from api import app
from flask import request  # Import the request object

class MyAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config["TESTING"] = True

    def test_index_page(self):
        with app.app_context():
            response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_get_people(self):
        with app.app_context():
            response = self.app.get("/people")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.data.decode())

    def test_get_people_by_id(self):
        with app.app_context():
            response = self.app.get("/people/2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Jane" in response.data.decode())


    def test_create_person(self):
        with app.app_context():
            response = self.app.post("/people", json={"first_name": "Alice", "last_name": "Smith", "age": 30, "city": "New York"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Person created successfully", response.data.decode())

    def test_update_person(self):
        with app.app_context(): 
            response = self.app.put(
                "/people/1",
                json={"first_name": "Bob", "last_name": "Johnson", "age": 35, "city": "Los Angeles"}
            )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person updated successfully", response.data.decode())

    def test_delete_person(self):
        with app.app_context():
            response = self.app.delete("/people/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Person deleted successfully", response.data.decode())


if __name__ == "__main__":
    unittest.main()
