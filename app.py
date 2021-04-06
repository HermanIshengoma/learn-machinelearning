from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, jsonify, session
from flask_bootstrap import Bootstrap
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
from database import Database
from dotenv import load_dotenv, find_dotenv

import constants

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

app = Flask(__name__)
app.secret_key = constants.SECRET_KEY
app.debug = True

@app.errorhandler(Exception)
def handle_auth_error(ex):
	print('auth-error')
	response = jsonify(message=str(ex))
	response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
	return response

oauth = OAuth(app)

auth0 = oauth.register(
	'auth0',
	client_id=AUTH0_CLIENT_ID,
	client_secret=AUTH0_CLIENT_SECRET,
	api_base_url=AUTH0_BASE_URL,
	access_token_url=AUTH0_BASE_URL + '/oauth/token',
	authorize_url=AUTH0_BASE_URL + '/authorize',
	client_kwargs={
		'scope': 'openid profile email',
	},
)

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		print("requires_auth")
		if constants.PROFILE_KEY not in session:
			return redirect('/index')
		return f(*args, **kwargs)

	return decorated

# intro page
@app.route('/', methods=['GET'])
def start_page():
	print('start page11')
	html = render_template('index.html')
	return html


@app.route('/callback')
def callback_handling():
	auth0.authorize_access_token()
	resp = auth0.get('userinfo')
	userinfo = resp.json()

	session[constants.JWT_PAYLOAD] = userinfo
	session[constants.PROFILE_KEY] = {
		'user_id': userinfo['sub'],
		'name': userinfo['name'],
		'picture': userinfo['picture']
	}

    # dealing with the database
	database = Database(app)
	database.connect()
	userinfo=session[constants.PROFILE_KEY]
	user_id=userinfo['user_id']

	success = database.user_exist(user_id)
	if success is False:
		new_username = "Stranger"
		database.update_username(new_username, user_id)
	database.disconnect()

	return redirect('/main')


@app.route('/login')
def login():
	return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
	session.clear()
	params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
	return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


# linear algebra module
@app.route('/main', methods=['GET'])
def main_page():
	html = render_template('main.html')
	return html

# numpy module
@app.route('/numpy', methods=['GET'])
def numpy_page():
	html = render_template('numpy.html')
	return html

# programming module
@app.route('/programming', methods=['GET'])
def programming_page():
	html = render_template('programming.html')
	return html

if __name__ == "__main__":
	app.run()