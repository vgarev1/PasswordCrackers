import pyperclip
from flask import Flask, jsonify

app = Flask(__name__)
password_generator = PasswordGenerator()
stored_password = ""  # Store the last generated password

@app.route('/copy-password', methods=['POST'])
def copy_password():
    global stored_password
    if stored_password:
        pyperclip.copy(stored_password)
        return jsonify({"message": "Password copied to clipboard!"})
    return jsonify({"error": "No password to copy"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
