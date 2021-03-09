from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, jsonify, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_page():
	html = render_template('index.html')
	return html

@app.route('/main', methods=['GET'])
def main_page():
	html = render_template('main.html')
	return html

if __name__ == "__main__":
	app.run()