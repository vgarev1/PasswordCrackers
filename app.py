from flask import Flask, request, jsonify, abort, render_template, redirect, url_for  #Flask - creates web application; request - gets data from the incoming requests; jsonify - returns JSON responses; abort - sends error codes if something is wrong
from flask_pymongo import PyMongo  #PyMongo - Flask extention which makes it easier to work with MongoDB
from bson.objectid import ObjectId  #ObjectId - converts string IDs to MongoDB's native ID type
from markupsafe import escape
from hashlib import sha512
from pass_generator import PasswordGenerator
import database

app = Flask(__name__)  #creates a new Flask object which represents the web application

@app.route('/', methods=['GET'])
def index_page():
    invalid_info = False

    if "invalid" in request.args:
        if request.args["invalid"] == "True":
            invalid_info = True

    return render_template("index.html", invalid=invalid_info)

@app.route('/signup-page', methods=['GET'])
def signup_page():
    return render_template("signup.html")

@app.route('/display-page', methods=['POST'])
def display_page():
    users_collection = database.get_users()

    users_dict = dict()

    for user_info in users_collection:
        users_dict[user_info["username"]] = user_info["password"]

    input_username = request.form["username"]
    input_password = sha512(bytes(request.form["password"], encoding='utf-8')).hexdigest()

    if (input_username in users_dict):
        if (users_dict[input_username] == input_password):
            pass

        else:
            return redirect(url_for('index_page') + "?invalid=True")

    else:
        return redirect(url_for('index_page') + "?invalid=True")

    return render_template("display.html", username=input_username)

@app.route('/create-page', methods=['GET'])
def create_page():
    return render_template("create.html")

@app.route('/generate', methods=['POST'])
def generate():
    # Get user inputs from form
    length = int(request.form.get('length', 12))
    use_upper = 'uppercase' in request.form
    use_lower = 'lowercase' in request.form
    use_number = 'number' in request.form
    use_special = 'special' in request.form
    site = request.form.get('site-name', 'N/A')

    # Setup generator with user settings
    gen = PasswordGenerator()
    gen.maxlen = length
    gen.minlen = length
    gen.minuchars = 1 if use_upper else 0
    gen.minlchars = 1 if use_lower else 0
    gen.minnumbers = 1 if use_number else 0
    gen.minschars = 1 if use_special else 0

    # If no options selected show error
    if gen.minuchars + gen.minlchars + gen.minnumbers + gen.minschars == 0:
        return "Error: You must select at least one character type."

    # Generate the password
    password = gen.generate()

    # Render result page with password and site
    return render_template('result.html', password=password, site=site)

@app.route('/delete-page', methods=['GET', 'POST'])
def delete_page():
    return render_template("delete.html")

@app.route('/new-user-page', methods=['POST'])  #URL endpoint that accepts "POST" requests to users
#Function for creating a new user
def create_user():
    users_collection = database.get_users()

    users_list = list()

    for user_info in users_collection:
        users_list.append(user_info["username"])

    input_username = request.form["name"]

    input_success = True

    if input_username in users_list:
        input_success = False

    else:
        input_password = sha512(bytes(request.form["password"], encoding='utf-8')).hexdigest()

        database.create_user(input_username, input_password)

    return render_template("new_user.html", success=input_success, username=escape(input_username))

"""
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
"""

if __name__ == "__main__":
    app.run()