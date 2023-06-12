from flask import Flask, render_template, request, send_file, jsonify, make_response, send_from_directory
from logging.config import dictConfig
import json
from application.lottery import Lottery

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config.from_object('application.config.Config')

flag = open("/flag.txt").read()

@app.route('/',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/api/guess',methods=['POST'])
def guess():

    J = request.get_json()

    if J is None:
        return make_response(jsonify({"error":"Invalid JSON Request"}))

    g = J.get('guess',None)

    if g is None:
        return make_response(jsonify({"error":"No Guess Provided"}))
    try:
        g = int(g)
    except ValueError:
        return make_response(jsonify({"error":"Invalid Number Given"}))

    L = Lottery()
    draw = L.draw()

    if g == draw:
        return make_response(jsonify({"success":"Congrats! The flag is: %s" % flag}))
    else:
        return make_response(jsonify({"fail":"Sorry, better luck next time!"}))

@app.route('/api/recent',methods=['GET'])
def recent(): 
    L = Lottery()
    R = L.last_n_draws(10)
    return make_response(jsonify(R))

@app.route('/favicon.ico',methods=['GET'])
def icon():
    return send_file("static/favicon.ico")


@app.route('/.git/<path:path>')
def send_git(path):
    return send_from_directory('git', path)
        
        
    



