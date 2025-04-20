from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["password_generator"]
users_collection = db["users"]
passwords_collection = db["passwords"]

# Function to create a new user
def create_user(username, hashed_password):
    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        return None  # Username already exists
    user = {
        "username": username,
        "password": hashed_password,  # Store hashed passwords
        "created_at": datetime.utcnow()
    }
    return users_collection.insert_one(user).inserted_id

# Function to validate login credentials
def validate_user(username, password):
    # Find the user in the database by username
    user = users_collection.find_one({"username": username})
    if user:
        # Check if the provided password matches the hashed password in the database
        if check_password_hash(user["password"], password):
            return str(user["_id"])  # Return the user ID if valid
    return None  # Return None if the username or password is invalid

# Function to store a generated password
def store_password(user_id, password, strength, site):
    password_entry = {
        "user_id": ObjectId(user_id),
        "password": password,  # Encrypt this before storing in production
        "strength": strength,
        "site": site,  # Store the site name
        "created_at": datetime.utcnow()
    }
    return passwords_collection.insert_one(password_entry).inserted_id

# Function to retrieve a user's password history
def get_password_history(user_id):
    return list(passwords_collection.find(
        {"user_id": ObjectId(user_id)},
        {"_id": 0, "password": 1, "strength": 1, "site": 1, "created_at": 1}
    ))

# Function to delete a password entry
def delete_password(user_id, password):
    result = passwords_collection.delete_one({
        "user_id": ObjectId(user_id),
        "password": password
    })
    return result.deleted_count > 0  # Return True if a document was deleted