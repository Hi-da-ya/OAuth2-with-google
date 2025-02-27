# OAuth2 and OpenID Connect (OIDC) Authentication with Google in Flask
## Overview
This project implements OAuth2 and OpenID Connect (OIDC) authentication using Google in a Flask application. It allows users to log in with their Google accounts, retrieve profile information, and manage sessions securely.

## Features
- OAuth2-based authentication with Google
- Secure token exchange and user session management
- User information retrieval (email, profile picture, name)
- SQLite database for storing authenticated users
- Flask-Login for session handling

## Prerequisites
Ensure you have the following installed before setting up the project:
- Python 3
- Flask
- SQLite
- Google Cloud Console credentials (OAuth2 Client ID & Secret)

## Setup Instructions

### 1. Clone the Repository
```sh
git clone git@github.com:Hi-da-ya/OAuth2-with-google.git
cd oauth-flask-google
```

### 2. Create a Virtual Environment (Optional but Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirement.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory and add:
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SECRET_KEY=your_secret_key
SECURITY_PASSWORD_SALT=your_salt_value
```

### 5. Initialize the Database
```sh
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 6. Run the Flask Application
```sh
python3 app.py
```
Your application should be running at `https://127.0.0.1:5000/`.

## API Endpoints

### Home Route
**GET `/`**
- Displays a login button if the user is not authenticated
- Shows user details if logged in

### Google Login
**GET `/login`**
- Redirects user to Google’s OAuth2 authentication page

### Login Callback
**GET `/login/callback`**
- Handles Google’s OAuth2 response, retrieves user details, and logs them in

### Logout
**GET `/logout`**
- Logs the user out and redirects to home

## Code Overview
### Main Components:
- **`app.py`** – Handles the Flask application setup, routes, and authentication logic
- **`user.py`** – Defines the `User` model and database interactions
- **`.env`** – Stores sensitive credentials securely

## Troubleshooting
- If authentication fails, check your Google OAuth credentials in `.env`.
- Ensure Google Cloud Console has the correct redirect URIs (`http://127.0.0.1:5000/login/callback`).
- If the database isn't working, make sure `sqlite:///gusers.db` is accessible and `flask db upgrade` has been run.

## License
This project is open-source and available under the MIT License.
