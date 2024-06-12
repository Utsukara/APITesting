import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_sum(client, mocker):
    payload = {"num1": 1, "num2": 2}
    mocker.patch.object(client, 'post', return_value=app.response_class(
        response=json.dumps({"result": 3}),
        status=200,
        mimetype='application/json'
    ))
    response = client.post('/sum', json=payload)
    data = response.get_json()
    assert data['result'] == 3

# Run the test
# $ pytest test_mock.py
if __name__ == '__main__':
    pytest.main([__file__])