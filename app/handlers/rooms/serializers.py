from app.utils.validation_form import ValidationForm
from marshmallow import fields, Schema


class RoomsSerializer(ValidationForm):
    id = fields.Integer()
    room = fields.Integer()
    name = fields.Method('get_name')

    def get_name(self, obj):
        buildings = self.context.get('buildings', [])

        building = next((_ for _ in buildings if _.id == obj.building_id), None)

        return f"{obj.room} - {building.address} ({building.country})"


class RoomResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(RoomsSerializer, many=True, attribute='instances')
