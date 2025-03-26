import pytest
from flask import Flask, request, jsonify, abort
import mongomock
from werkzeug.security import generate_password_hash

app = Flask(__name__)
mock_db = mongomock.MongoClient().db
app.config['TESTING'] = True

#A function for registering a user with username and password
@app.route('/register', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    if not data or 'name' not in data or 'password' not in data:
        abort(400, description="Missing 'name' or 'password' in request data")

    hashed_pw = generate_password_hash(data['password'])
    user_data = {
        'name': data['name'],
        'password': hashed_pw
    }
    result = mock_db.users.insert_one(user_data)
    return jsonify({
        "message": "User created successfully",
        "id": str(result.inserted_id)
    }), 201

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

#Test Cases

def test_create_user_with_password(client):
    print("This test is running!")

    response = client.post('/register', json={
        'name': 'secureuser',
        'password': 'SafePassword123'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'User created successfully'
    assert 'id' in data
