import os
import traceback

from flask import Flask, jsonify
from app.main import Main
from flask_cors import CORS

from flask import request, session, request_finished, g

from app.utils.custom_exceptions import BadRequestAPIException, UnauthorizedAPIException
from configs.run_config import CONFIG

app = Main().create_app()

# cors = CORS(app, supports_credentials=True, origins=r"(.*){0}".format(CONFIG.UI_HOST))


@app.before_request
def before_request():
    g.tenant_host = os.environ.get('DB_HOST')

    token = request.headers.get("Authorization-token")
    user = CONFIG.USER_SERVICE.fetch(authorization_token=token)

    if not user and request.path not in ['/users/login']:
        raise UnauthorizedAPIException()
    # g.request_data = {**(request.args.to_dict() or {}), **(request.get_json() or {}), **(request.view_args or {})}
    # a = request.get_json()
    # g.request_data = {**(request.get_json() or {})}


@app.errorhandler(KeyError)
def custom_exception(e):
    CONFIG.PG_DB.session.rollback()

    traceback.print_exc()
    payload = {
        'success': False,
        'payload': {
            'code': 500,
            'params': request.args
        },
        'message': str(e)
    }
    response = jsonify(payload)
    response.status_code = 500
    return response


@app.errorhandler(Exception)
def exception(exception):
    CONFIG.PG_DB.rollback()

    traceback.print_exc()
    payload = {
        'success': False,
        'payload': [],
        'message': str(exception)
    }
    response = jsonify(payload)
    response.status_code = 500
    return response


@app.errorhandler(BadRequestAPIException)
def handle_400(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(UnauthorizedAPIException)
def handle_401(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # manager.run()
    app.run()

