from flask import jsonify


def response(payload, status_code=200):
    return jsonify({
        'status': status_code,
        'result': payload,
    }), status_code
