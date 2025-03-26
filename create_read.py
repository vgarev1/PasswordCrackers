from flask import Flask, request, jsonify, abort, render_template  #Flask - creates web application; request - gets data from the incoming requests; jsonify - returns JSON responses; abort - sends error codes if something is wrong
from flask_pymongo import PyMongo  #PyMongo - Flask extention which makes it easier to work with MongoDB
from bson.objectid import ObjectId  #ObjectId - converts string IDs to MongoDB's native ID type

app = Flask(__name__)  #creates a new Flask object which represents the web application
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)  #sets up a connection with MongoDB

@app.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")

@app.route('/signup-page', methods=['GET'])
def create_page():
    return render_template("signup.html")

@app.route('/display-page', methods=['GET', 'POST'])
def create_page():
    return render_template("display.html")

@app.route('/create-page', methods=['GET', 'POST'])
def create_page():
    return render_template("create.html")

@app.route('/result-page', methods=['GET'])
def create_page():
    return render_template("result.html")

@app.route('/delete-page', methods=['GET', 'POST'])
def create_page():
    return render_template("delete.html")

@app.route('/users', methods=['POST'])  #URL endpoint that accepts "POST" requests to users
#Function for creating a new user
def create_user():
    data = request.get_json(force=True)  #reads the incoming data
    #validation
    if not data or 'name' not in data:
        abort(400, description="Missing 'name' in request data")
    
    result = mongo.db.users.insert_one(data)  #inserts the new user into the database
    #returns the following message and the id of the new user and the '201' HTTP status code
    return jsonify({
        "message": "User created successfully",
        "id": str(result.inserted_id)
    }), 201 
  
@app.route('/users', methods=['GET'])  #URL endpoint that accepts "GET" requests to users
#Function for getting all the users from the database
def get_users():
    users = mongo.db.users.find()  #retrieves all the data from the database
    result = []
    #iteration for all id's of the users and converts all id's to a string (because MongoDB uses ObjectID, which is not directly JSON serializable)
    for user in users:
        user['_id'] = str(user['_id'])
        result.append(user)
    return jsonify(result)  #returns all the users that are in the database

if __name__ == "__main__":
    app.run()