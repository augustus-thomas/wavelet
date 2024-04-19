# flask app
from app import app
# REST API enabling library
from flask import render_template, Flask, jsonify, request, send_file
# async calls
import subprocess
import sys


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
    scripts_arguments = ["python3", "app/sim.py"] + [str(arg) for arg in list(args.values())]
    test = subprocess.run(scripts_arguments)
    # this is where we saved sim
    simulation_url = '/static/sim.mp4'
    # return link
    return jsonify({'sim_url': simulation_url})

# returning the static mp4 object
@app.route('/sim.mp4', methods=['GET'])
def render_video():
    return send_file('../static/sim.mp4', mimetype='video/mp4')