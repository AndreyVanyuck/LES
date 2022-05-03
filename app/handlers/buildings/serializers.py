from app.utils.validation_form import ValidationForm
from marshmallow import fields, Schema


class BuildingSerializer(ValidationForm):
    id = fields.Integer()
    name = fields.Method('get_name')

    @staticmethod
    def get_name(obj):
        return f"{obj.address} ({obj.country})"


class BuildingResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(BuildingSerializer, many=True, attribute='instances')
