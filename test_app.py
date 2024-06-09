import unittest
from app import app
from faker import Faker

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_sum(self):
        fake = Faker()
        num1 = fake.random_number(digits=2)
        num2 = fake.random_number(digits=2)
        payload = {"num1": num1, "num2": num2}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], num1 + num2)

if __name__ == '__main__':
    unittest.main()
