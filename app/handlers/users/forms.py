from app.utils.custom_exceptions import BadRequestAPIException, UnauthorizedAPIException
from app.utils.validation_form import ValidationForm
from marshmallow import fields, validate, Schema, validates, validates_schema
from app.main import CONFIG
from werkzeug.security import generate_password_hash, check_password_hash


class UserForm(ValidationForm):
    title = fields.String(required=True, validate=validate.OneOf(['Mr', 'Mrs']))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    first_name_native = fields.String(required=True)
    last_name_native = fields.String(required=True)
    middle_name_native = fields.String(required=True)
    department_id = fields.Integer(required=True)
    room_id = fields.Integer(required=False)
    email = fields.Email(required=True)
    mobile_phone = fields.Integer(required=True)
    building_id = fields.Integer(required=True)

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
    name = fields.String(required=False)
    email = fields.String(required=False)
    limit_ = fields.Integer(required=False, data_key='limit')
    offset_ = fields.Integer(required=False, data_key='offset')
    building_id = fields.Integer(required=False)
    room_id = fields.Integer(required=False)
    department_id = fields.Integer(required=False)
    is_manager = fields.Boolean(required=False)
    sort_ = fields.String(
        required=False,
        default='id',
        data_key='sort'
    )
