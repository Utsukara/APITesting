import unittest
from app import app, db, Sum
from faker import Faker

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()  # Create tables
            self.fake = Faker()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Drop tables

    def test_sum(self):
        num1 = self.fake.random_number(digits=2)
        num2 = self.fake.random_number(digits=2)
        payload = {"num1": num1, "num2": num2}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        print(f"Test sum with payload: {payload} -> result: {data['result']}")
        self.assertEqual(data['result'], num1 + num2)

    def test_negative_sum(self):
        payload = {"num1": -5, "num2": -10}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        print(f"Test negative sum with payload: {payload} -> result: {data['result']}")
        self.assertEqual(data['result'], -15)

if __name__ == '__main__':
    unittest.main()
