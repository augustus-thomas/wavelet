# flask app
from app import app
# REST API enabling library
from flask import render_template, Flask, jsonify, request
# file structure?
import os
# async calls
import subprocess

# home page
@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    # create the HTML from template
    return render_template("index.html")

# running the simulation with script.py asynchronously
@app.route('/start_sim', methods=['POST'])
def run_sim():
    # get arguments
    args = request.json
    # ???
    # run sim async
    scripts_arguments = ["python3", "sim.py"]
    subprocess.run(['python3', 'script.py'])
    # this is where we saved sim
    simulation_url = '/static/sim.mp4'
    # return link
    return jsonify({'sim_url': simulation_url})