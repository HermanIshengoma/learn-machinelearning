from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, jsonify, session

app = Flask(__name__)


@app.route('/', methods=['GET'])
def start_page():
	html = render_template('index.html')
	return html


if __name__ == "__main__":
	app.run()