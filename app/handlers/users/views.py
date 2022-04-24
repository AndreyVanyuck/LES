from flask import Blueprint, request

from app.handlers.users.forms import UserForm
from app.handlers.users.serializers import UserResponseSerializer

from app.main import CONFIG
from app.utils.response_formatting import response

USERS_BLUEPRINT = Blueprint('user', __name__)


@USERS_BLUEPRINT.route("/users/create", methods=['POST'])
def create_user():
    form = UserForm().load(request.get_json())
    service = CONFIG.USER_SERVICE
    serializer = UserResponseSerializer()

    form['is_admin'] = False
    instances = service.create(**form)

    result = serializer.dump({
        'total_count': 1,
        'instances': [instances]
    })

    return response(result)


@USERS_BLUEPRINT.route("/users", methods=['GET'])
def get_users():
    service = CONFIG.USER_SERVICE
    serializer = UserResponseSerializer()

    instances = service.fetch_all()

    result = serializer.dump({
        'total_count': len(instances),
        'instances': instances
    })

    return response(result)
