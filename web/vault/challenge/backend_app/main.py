from flask import Flask, render_template, request, Response, send_file, jsonify, make_response, abort
from logging.config import dictConfig
import json

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


@app.route('/',methods=['GET'])
def index():
    return "Vault backend service is running."

@app.route('/download',methods=['GET'])
def download():
    return send_file("file.zip")
        
        
    



