import json
import os
from datetime import timedelta
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_mail import Mail

#Third party libraries
from flask import Flask, redirect,request, url_for
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from user import db, User

#Load env variables
load_dotenv()

#Configure google credentials
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

#Set up flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///gusers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)
app.config['SECURITY_PASSWORD_SALT']= os.getenv('SECURITY_PASSWORD_SALT')

#OAuth2 client set up
client = WebApplicationClient(GOOGLE_CLIENT_ID)


migrate = Migrate(app,db)
mail = Mail(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Views and Routes

@app.route('/')
def home():
    if current_user.is_authenticated:
        return(
            "<h4>Hello, {}! You're logged in!</h4>"
            "<h5>Email: {}</h5>"
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email
            )
        )
    else:
        return '<a class="button" href="/login">Login with Google</a>'

#Google client configuration
def get_google_config():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

#Login route
@app.route('/login')
def login():
    google_provider_config = get_google_config()
    authorization_endpoint = google_provider_config["authorization_endpoint"]     

    # Use oauthlib library to construct the request for Google login and provide scopes that
    #let you retrieve user's profile from Google

    redirect_uri = request.base_url + "/callback" 

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri = redirect_uri,
        scope = ["openid", "email", "profile"]
    )

    return redirect(request_uri)

#Login callback
@app.route('/login/callback')
def callback():
    #Get authorization code that Google sends back
    auth_code = request.args.get("code")

    #Figure out what Google's token endpoint is
    google_provider_confg = get_google_config()
    token_endpoint = google_provider_confg["token_endpoint"]

    #Prepare and send request to get token
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=auth_code
    )

    token_response = requests.post(
        token_url,
        headers = headers,
        data = body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Retrieve user information from google
    user_info_endpoint = google_provider_confg["userinfo_endpoint"]
    uri, headers, body = client.add_token(user_info_endpoint)
    user_info_response = requests.get(
        uri,
        headers=headers,
        data=body
    )

    #Parse the response received from user info endpoint
    if user_info_response.json().get("email_verified"):
        unique_id = user_info_response.json()["sub"]
        users_email = user_info_response.json()["email"]
        picture = user_info_response.json()["picture"]
        users_name = user_info_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    #Create user in db using information from Google
    new_user = User(
        id = unique_id,
        email = users_email,
        fullname = users_name,
        profile_pic = picture

    )

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect(url_for("home"))

#Logout function
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
        