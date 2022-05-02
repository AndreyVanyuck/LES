from flask import Blueprint, request, g

from app.handlers.requests.forms import RequestCreateForm, RequestsListFetchForm, RequestUpdateForm
from app.handlers.requests.serializers import RequestResponseSerializer

from app.main import CONFIG
from app.utils.response_formatting import response

REQUESTS_BLUEPRINT = Blueprint('request', __name__)


@REQUESTS_BLUEPRINT.route("/requests/create", methods=['POST'])
def create_request():
    form = RequestCreateForm().load(request.get_json())
    service = CONFIG.CREATE_REQUEST_SERVICE
    serializer = RequestResponseSerializer()

    form['user_id'] = g.user_id
    instance = service.create(**form)

    # TODO send emails

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@REQUESTS_BLUEPRINT.route("/requests", methods=['GET'])
def get_request():
    form = RequestsListFetchForm().load(request.args)
    service = CONFIG.REQUEST_SERVICE
    serializer = RequestResponseSerializer()

    instances = service.fetch_all(**form)

    # TODO send emails

    result = serializer.dump({
        'total_count': len(instances),
        'instances': instances
    })

    return response(result)


@REQUESTS_BLUEPRINT.route("/requests/<id>", methods=['PUT'])
def update_request(id):
    form = RequestUpdateForm().load(request.get_json())
    service = CONFIG.UPDATE_REQUEST_SERVICE
    serializer = RequestResponseSerializer()

    instance = service.update(pk=id, user_id=g.user_id, **form)

    # TODO send emails

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@REQUESTS_BLUEPRINT.route("/requests/cancel/<pk>", methods=['POST'])
def cancel_request(pk):
    service = CONFIG.UPDATE_REQUEST_SERVICE
    serializer = RequestResponseSerializer()

    instance = service.cancel_request(pk=pk)

    # TODO send emails

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)
