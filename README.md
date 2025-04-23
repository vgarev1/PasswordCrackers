# Password Generator Website
A full-stack password generator web application that enables users to create secure, customizable passwords. The application includes an intuitive interface for selecting password length and characteristics (numbers, special characters, uppercase/lowercase letters) with a copy-to-clipboard functionality. It features a password strength test and stores generated passwords in a database to prevent duplicates and provide a history of previously created passwords.
## Usage (Step-by-Step)
1. Visit the website:

2. Create an account (Optional):
   - Username
   - First name
   - Last name
   - Email
   - Password

3. Configure password criteria:
   - Password length
   - Character options: uppercase/lowercase letters, numbers, special characters

4. Generate password by clicking the "generate" button

5. Check and use the generated password:
   - Generated password will be shown
   - "Copy" button to copy the password to the clipboard
   - Generate another password
   - Save the password to your existing account for future use


PasswordCrackers/
├── app.py                     # Main Flask application
├── README.md                  # Project documentation
├── backend/                   # Backend logic and database interaction
│   ├── copy_to_clipboard.py   # Handles clipboard functionality
│   ├── create_read.py         # Handles creation and reading of data
│   ├── database.py            # Database connection and queries
│   ├── pass_generator.py      # Password generation logic
├── frontend/                  # Frontend templates and static assets
│   ├── templates/             # HTML templates
│   │   ├── create.html        # Password creation form
│   │   ├── delete.html        # Delete password page
│   │   ├── display.html       # Display saved passwords
│   │   ├── help1.html         # Help page 1
│   │   ├── index.html         # Homepage
│   │   ├── result.html        # Password generation result page
│   │   ├── signup.html        # Signup form
│   ├── static/                # Static assets (CSS, JS, images)
│       ├── css/
│       │   └── layout.css     # Stylesheet for the application
│       ├── js/
│       │   ├── help2.js       # JavaScript for help page 2
│       │   └── script.js      # Main JavaScript file
│       └── images/
│           └── background.jpg # Background image

## Setup and Running the Application

### Starting the MongoDB Server
To start the MongoDB server with your custom configuration file, run the following command:
```bash
mongod --config ~/mongod.conf