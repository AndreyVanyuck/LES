from app.utils.custom_exceptions import BadRequestAPIException, UnauthorizedAPIException
from app.utils.validation_form import ValidationForm
from marshmallow import fields, validate, Schema, validates, validates_schema
from app.main import CONFIG
from werkzeug.security import generate_password_hash, check_password_hash


class UserForm(ValidationForm):
    title = fields.String(validate=validate.OneOf(['Mr', 'Ms']))
    first_name = fields.String()
    last_name = fields.String()
    first_name_native = fields.String()
    last_name_native = fields.String()
    middle_name_native = fields.String()
    department_id = fields.Integer()
    room_id = fields.Integer()
    email = fields.Email()
    mobile_phone = fields.Integer()
    building_id = fields.Integer()

    @validates('department_id')
    def validated_department_id(self, value):
        service = CONFIG.DEPARTMENT_SERVICE
        if not service.exists(id=value):
            raise BadRequestAPIException(
                payload={'error_code': 'department_id_not_found', 'params': [value]}
            )


class UserCreateForm(UserForm):
    @validates('email')
    def validated_email(self, value):
        service = CONFIG.USER_SERVICE
        if service.exists(email=value):
            raise BadRequestAPIException(
                payload={'error_code': 'email_already_exist', 'params': [value]}
            )


class LoginForm(ValidationForm):
    email = fields.String(required=True)
    password = fields.String(required=True)

    @validates('email')
    def validated_email(self, value):
        service = CONFIG.USER_SERVICE
        if not service.exists(email=value):
            raise BadRequestAPIException(
                payload={'error_code': 'email_not_found', 'params': [value]}
            )

    @validates_schema
    def validate_password(self, data, **kwargs):
        user = CONFIG.USER_SERVICE.fetch(email=data.get('email'))
        password = data.get('password')

        if not user or not check_password_hash(user.authorization_token, password):
            raise UnauthorizedAPIException(
                payload={'error_code': 'unauthorized', 'params': []}
            )


class UserIdForm(ValidationForm):
    id = fields.Integer(required=True)

    @validates('id')
    def validated_id(self, value):
        service = CONFIG.USER_SERVICE
        if not service.exists(id=value):
            raise BadRequestAPIException(
                payload={'error_code': 'user_not_found', 'params': [value]}
            )


class UserListFetchForm(ValidationForm):
    search_ = fields.String(required=False, data_key='search')
    email = fields.String(required=False)
    limit_ = fields.Integer(required=False, data_key='limit')
    offset_ = fields.Integer(required=False, data_key='offset')
    building_id = fields.Integer(required=False)
    room_id = fields.Integer(required=False)
    department_id = fields.Integer(required=False)
    is_manager = fields.Boolean(required=False)
    grouping = fields.String(required=False, default='', validate=validate.OneOf(['all', 'on_a_leave', 'require_approval']))
    sort_ = fields.String(
        required=False,
        default='id',
        data_key='sort'
    )
