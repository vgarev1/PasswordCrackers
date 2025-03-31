from flask import Flask, render_template, request
from pass_generator import PasswordGenerator 

app = Flask(__name__)

@app.route('/')
def create():
    return render_template('create.html')

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

if __name__ == '__main__':
    app.run(debug=True)
