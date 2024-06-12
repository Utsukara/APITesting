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

    def test_get_sums_by_result(self):
        # Add some sums
        sums = [(1, 3), (2, 2), (-1, 5), (3, 1)]
        for num1, num2 in sums:
            result = num1 + num2
            payload = {"num1": num1, "num2": num2}
            self.app.post('/sum', json=payload)
        
        response = self.app.get('/sum/result/4')
        data = response.get_json()
        print(f"Test get sums by result=4 -> result: {data}")
        self.assertEqual(len(data), 2)  # Expecting two results: (1, 3) and (2, 2)

    def test_invalid_get_sums_by_result(self):
        response = self.app.get('/sum/result/not_a_number')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
