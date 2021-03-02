from flask import Flask, request, make_response, redirect, url_for
from flask import render_template, jsonify, session

app = Flask(__name__)


@app.route('/')
def start_page():
	html = render_template('index.html')
	return make_response(html)


if __name__ == "__main__":
	app.run()