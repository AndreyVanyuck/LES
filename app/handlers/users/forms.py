from app.utils.custom_exceptions import BadRequestAPIException
from app.utils.validation_form import ValidationForm
from marshmallow import fields, validate, Schema, validates
from app.main import CONFIG


class UserForm(ValidationForm):
    title = fields.String(required=True, validate=validate.OneOf(['mr', 'mrs']))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    first_name_native = fields.String(required=True)
    last_name_native = fields.String(required=True)
    middle_name_native = fields.String(required=True)
    department_id = fields.Integer(required=True)
    room = fields.Float(required=True)
    email = fields.String(required=True)
    mobile_phone = fields.Integer(required=True)

    @validates('department_id')
    def validated_external_id(self, value):
        service = CONFIG.DEPARTMENT_SERVICE
        if not service.exists(id=value):
            raise BadRequestAPIException(
                payload={'error_code': 'department_id_not_found', 'params': [value]}
            )
