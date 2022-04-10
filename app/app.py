from flask import Flask
from app.main import Main
from flask_cors import CORS
from app.main import CONFIG
from flask import request, session, request_finished, g

# app = Main().app#create_app()
app = Flask(__name__)
# cors = CORS(app, supports_credentials=True, origins=r"(.*){0}".format(CONFIG.UI_HOST))


@app.before_request
def before_request():
    g.request_data = {**(request.args.to_dict() or {}), **(request.get_json() or {}), **(request.view_args or {})}


@app.route('/')
def hello_world():
    a = 1# put application's code here
    return 'Hello World!'
