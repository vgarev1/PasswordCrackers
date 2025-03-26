import pytest
from flask import Flask, request, jsonify, abort
import mongomock
from werkzeug.security import check_password_hash, generate_password_hash

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

#A function checking if user credentials match
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    if not data or 'name' not in data or 'password' not in data:
        abort(400, description="Missing 'name' or 'password' in request data")

    user = mock_db.users.find_one({'name': data['name']})
    if user and check_password_hash(user['password'], data['password']):
        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id'])
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

#Test Cases

def test_login_user_with_correct_password(client):
    #Register the user first
    client.post('/register', json={
        'name': 'usernametest',
        'password': 'Secret123'
    })

    #Try login with correct credentials
    response = client.post('/login', json={
        'name': 'usernametest',
        'password': 'Secret123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Login successful'
    assert 'user_id' in data

def test_login_user_with_wrong_password(client):
    #Register the user
    client.post('/register', json={
        'name': 'wrongpassuser',
        'password': 'CorrectPass123'
    })

    #Try logging in with wrong password
    response = client.post('/login', json={
        'name': 'wrongpassuser',
        'password': 'WrongPass123'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Invalid credentials'
