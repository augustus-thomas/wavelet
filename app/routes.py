from app import app
from flask import render_template, Flask
import os

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")