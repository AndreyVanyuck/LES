from app.utils.validation_form import ValidationForm
from marshmallow import fields, Schema
from app.main import CONFIG


class UserSerializer(ValidationForm):
    title = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    first_name_native = fields.String()
    last_name_native = fields.String()
    middle_name_native = fields.String()
    room = fields.Float()
    email = fields.String()
    mobile_phone = fields.Integer()
    is_admin = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    department = fields.Method('get_department')

    @staticmethod
    def get_department(obj):
        department = CONFIG.DEPARTMENT_SERVICE.fetch(id=obj.department_id)
        return {
            'id': department.id,
            'name': department.name
        }


class UserResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(UserSerializer, many=True, attribute='instances')
