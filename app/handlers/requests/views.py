from flask import Blueprint, request, g

from app.handlers.requests.forms import RequestCreateForm

from app.main import CONFIG
from app.utils.response_formatting import response

REQUESTS_BLUEPRINT = Blueprint('request', __name__)


@REQUESTS_BLUEPRINT.route("/requests/create", methods=['POST'])
def create_request():
    form = RequestCreateForm().load(request.get_json())
    service = CONFIG.CREATE_REQUEST_SERVICE
    # serializer = UserResponseSerializer()

    form['user_id'] = g.user_id
    instance = service.create(**form)

    # TODO send emails

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)
