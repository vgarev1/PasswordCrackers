from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["password_generator"]
users_collection = db["users"]
passwords_collection = db["passwords"]

# Function to create a new user
def create_user(username, hashed_password):
    user = {
        "username": username,
        "password": hashed_password,  # Store hashed passwords
        "created_at": datetime.utcnow()
    }
    return users_collection.insert_one(user).inserted_id

# Function to store a generated password
def store_password(user_id, password, strength):
    password_entry = {
        "user_id": ObjectId(user_id),
        "password": password,  # Encrypt this before storing in production
        "strength": strength,
        "created_at": datetime.utcnow()
    }
    return passwords_collection.insert_one(password_entry).inserted_id

# Function to retrieve a user's password history
def get_password_history(user_id):
    return list(passwords_collection.find({"user_id": ObjectId(user_id)}, {"_id": 0, "password": 1, "strength": 1, "created_at": 1}))

# Example Usage
if __name__ == "__main__":
    user_id = create_user("testuser", "hashed_test_password")
    print(f"User Created with ID: {user_id}")
    
    password_id = store_password(user_id, "P@ssw0rd123", "Strong")
    print(f"Stored Password with ID: {password_id}")
    
    history = get_password_history(user_id)
    print("Password History:", history)
