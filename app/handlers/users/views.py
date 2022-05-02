from flask import Blueprint, request, g

from app.handlers.users.forms import LoginForm, UserCreateForm, UserIdForm, UserListFetchForm, UserForm
from app.handlers.users.serializers import UserResponseSerializer, UserLoginResponseSerializer, UsersResponseSerializer, \
     UserVacationDayResponseSerializer

from app.main import CONFIG
from app.utils.response_formatting import response

USERS_BLUEPRINT = Blueprint('user', __name__)


@USERS_BLUEPRINT.route("/users/create", methods=['POST'])
def create_user():
    form = UserCreateForm().load(request.get_json())
    service = CONFIG.USER_SERVICE
    serializer = UserResponseSerializer()

    form['is_admin'] = False
    instance = service.create(**form)

    # TODO send email with password for user

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@USERS_BLUEPRINT.route("/users", methods=['GET'])
def get_users():
    form = UserListFetchForm().load(request.args)
    service = CONFIG.USER_SERVICE
    serializer = UsersResponseSerializer()

    instances = service.fetch_all(**form)

    serializer.context = {
        'departments': CONFIG.DEPARTMENT_SERVICE.fetch_all(
            in_and_={'id': list({_.department_id for _ in instances})}
        ),
        'rooms': CONFIG.ROOM_SERVICE.fetch_all(
            in_and_={'id': list({_.room_id for _ in instances})}
        ),
        'buildings': CONFIG.BUILDING_SERVICE.fetch_all(
            in_and_={'id': list({_.building_id for _ in instances})}
        )
    }

    result = serializer.dump({
        'total_count': len(instances),
        'instances': instances
    })

    return response(result)


@USERS_BLUEPRINT.route("/users/<pk>", methods=['GET'])
def get_user(pk):
    form = UserIdForm().load({'id': pk})
    service = CONFIG.USER_SERVICE
    serializer = UserResponseSerializer()

    instance = service.fetch(**form)

    serializer.context = {
        'departments': [CONFIG.DEPARTMENT_SERVICE.fetch(id=instance.department_id)],
        'rooms': [CONFIG.ROOM_SERVICE.fetch(id=instance.room_id)],
        'buildings': [CONFIG.BUILDING_SERVICE.fetch(id=instance.building_id)]
    }

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@USERS_BLUEPRINT.route("/users/<pk>", methods=['PATCH'])
def update_user(pk):
    form = UserForm().load(request.get_json())
    service = CONFIG.USER_SERVICE
    serializer = UserResponseSerializer()

    service.update(pk=pk, **form)
    instance = service.fetch(id=pk)

    serializer.context = {
        'departments': [CONFIG.DEPARTMENT_SERVICE.fetch(id=instance.department_id)],
        'rooms': [CONFIG.ROOM_SERVICE.fetch(id=instance.room_id)],
        'buildings': [CONFIG.BUILDING_SERVICE.fetch(id=instance.building_id)]
    }

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@USERS_BLUEPRINT.route("/users/login", methods=['POST'])
def login_user():
    form = LoginForm().load(request.get_json())
    service = CONFIG.USER_SERVICE
    serializer = UserLoginResponseSerializer()

    instance = service.fetch(email=form['email'])

    serializer.context = {
        'departments': [CONFIG.DEPARTMENT_SERVICE.fetch(id=instance.department_id)],
        'rooms': [CONFIG.ROOM_SERVICE.fetch(id=instance.room_id)],
        'buildings': [CONFIG.BUILDING_SERVICE.fetch(id=instance.building_id)]
    }

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@USERS_BLUEPRINT.route("/users/remained_days/<pk>", methods=['GET'])
def user_remained_days(pk):
    service = CONFIG.VACATION_DAY_CALCULATION_SERVICE
    serializer = UserVacationDayResponseSerializer()

    instance = service.get_remained_days(user_id=pk)

    result = serializer.dump({
        'total_count': 1,
        'instances': [instance]
    })

    return response(result)


@USERS_BLUEPRINT.route("/users/logout", methods=['POST'])
def logout_user():
    serializer = UserLoginResponseSerializer()

    result = serializer.dump({
        'total_count': 0,
        'instances': []
    })

    return response(result)
