from flask import Flask, render_template, request, Response, send_file, jsonify, make_response, abort
from logging.config import dictConfig
import requests

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
    return render_template("index.html")

@app.route('/download',methods=['POST'])
def download():

    vault_path = request.headers.get("x-vault-server",None)

    if vault_path is None:
        return make_response(jsonify({"error":"Missing vault server."}))
    
    # Fake it
    vault_path = vault_path.replace("backend.vault.uscg","127.0.0.1")
    
    if vault_path[:7] != "http://":
        vault_path = "http://" + vault_path
    try:
        R = requests.get(vault_path)

        if R.status_code == 200:
            return R.content
        else:
            return abort(500)
    except:
        return abort(500)

@app.route('/vault_key',methods=['GET'])
def vault_key():
    
    if request.remote_addr != "127.0.0.1":
        return "<h1>Access Denied from IP %s</h1>" % request.remote_addr
    
    return "Current Vault Password: liiJzuICLxAZqfb"

@app.route('/favicon.ico',methods=['GET'])
def icon():
    return send_file("static/favicon.ico")


@app.route('/robots.txt',methods=['GET'])
def robots():
    return send_file("robots.txt")
        
        
    



