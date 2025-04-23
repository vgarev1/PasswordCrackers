from flask import Flask, render_template, request, redirect, url_for, session
from backend.database import create_user, validate_user, store_password, get_password_history
from werkzeug.security import generate_password_hash, check_password_hash

# Explicitly set the template folder to "frontend/templates"
app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static") 
app.secret_key = "your_secret_key"  # Replace with a secure random key

@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from the form
    username = request.form.get('username')
    password = request.form.get('password')

    # Validate credentials in MongoDB
    user_id = validate_user(username, password)
    if user_id:
        # Store user ID in session
        session['user_id'] = user_id

        # Redirect to the dashboard page on successful login
        return redirect(url_for('dashboard', user_id=user_id))
    else:
        # Show an error message on invalid login
        return "Invalid username or password. Please try again.", 401

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    # Check if the user is logged in
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('login_page'))
    # Render the dashboard.html page with user_id
    return render_template('dashboard.html', user_id=user_id)

@app.route('/create/<user_id>', methods=['GET', 'POST'])
def create(user_id):
    # Render the create.html page
    return render_template('create.html', user_id=user_id)

@app.route('/generate/<user_id>', methods=['POST'])
def generate(user_id):
    # Get user inputs from the form
    length = int(request.form.get('length', 12))
    use_upper = 'uppercase' in request.form
    use_lower = 'lowercase' in request.form
    use_number = 'number' in request.form
    use_special = 'special' in request.form
    site = request.form.get('site-name', 'N/A')

    # Generate the password based on the parameters
    from backend.pass_generator import PasswordGenerator
    gen = PasswordGenerator()
    gen.maxlen = length
    gen.minuchars = 1 if use_upper else 0
    gen.minlchars = 1 if use_lower else 0
    gen.minnumbers = 1 if use_number else 0
    gen.minschars = 1 if use_special else 0

    # If no options are selected, show an error
    if gen.minuchars + gen.minlchars + gen.minnumbers + gen.minschars == 0:
        return "Error: You must select at least one character type."

    # Generate the password
    password = gen.generate()

    # Calculate password strength
    strength = gen.calculate_strength(password)

    # Store the password in the database
    store_password(user_id, password, strength,site)  # Assuming "Strong" for simplicity

    # Render the display.html page with the generated password and site name
    return render_template('display.html', password=password, site=site, strength=strength, user_id=user_id)

@app.route('/view_passwords/<user_id>')
def view_passwords(user_id):
    # Retrieve password history for the user
    history = get_password_history(user_id)
    return render_template('view_passwords.html', history=history, user_id=user_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get username, email, and password from the form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user in the database
        user_id = create_user(username, email, hashed_password)
        if user_id:
            return redirect(url_for('login_page'))
        else:
            return "Username or email already exists. Please choose a different one.", 400

    return render_template('signup.html')

@app.route('/delete_password/<user_id>', methods=['POST'])
def delete_password(user_id):
    # Get the password to delete from the form
    password = request.form.get('password')

    # Delete the password from the database
    from backend.database import delete_password
    success = delete_password(user_id, password)

    if success:
        return redirect(url_for('view_passwords', user_id=user_id))
    else:
        return "Error: Password could not be deleted.", 400
    
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)