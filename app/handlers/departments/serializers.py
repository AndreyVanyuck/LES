from app.utils.validation_form import ValidationForm
from marshmallow import fields, Schema


class DepartmentSerializer(ValidationForm):
    id = fields.Integer()
    name = fields.String()


class DepartmentResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(DepartmentSerializer, many=True, attribute='instances')
