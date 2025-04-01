from pymongo import MongoClient
from datetime import datetime, timezone
from bson.objectid import ObjectId

# Connect to MongoDB
def client_open():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["password_generator"]

    return (client, db)

# Function to create a new user
def create_user(username, hashed_password):
    client, db = client_open()

    user = {
        "username": username,
        "password": hashed_password,  # Store hashed passwords
        "created_at": datetime.now(timezone.utc)
    }

    inserted_id = db["users"].insert_one(user).inserted_id

    client.close()

    return inserted_id

# Function to store a generated password
def store_password(user_id, password, strength):
    client, db = client_open()

    password_entry = {
        "user_id": ObjectId(user_id),
        "password": password,  # Encrypt this before storing in production
        "strength": strength,
        "created_at": datetime.now(timezone.utc)
    }

    inserted_id = db["passwords"].insert_one(password_entry).inserted_id

    client.close()

    return inserted_id

def get_users():
    client, db = client_open()

    users_collection = db["users"].find({}).to_list()

    client.close()

    return users_collection

# Function to retrieve a user's password history
def get_user_password_history(user_id):
    client, db = client_open()

    passwords_collection = db["passwords"].find(
        {"user_id": ObjectId(user_id)}).to_list()

    client.close()

    return passwords_collection

# Example Usage
if __name__ == "__main__":
    user_id = create_user("testuser", "hashed_test_password")
    print(f"User Created with ID: {user_id}")

    password_id = store_password(user_id, "P@ssw0rd123", "Strong")
    print(f"Stored Password with ID: {password_id}")

    history = get_user_password_history(user_id)
    print("Password History:", history)