import json

from app.utils.validation_form import ValidationForm
from marshmallow import fields, Schema
from app.main import CONFIG


class RequestSerializer(ValidationForm):
    id = fields.Integer()
    request_type = fields.String()
    user_id = fields.Integer()
    created_at = fields.Date(format='%Y-%m-%d')
    start_date = fields.Date(format='%Y-%m-%d')
    end_date = fields.Date(format='%Y-%m-%d')
    comment = fields.String()
    state = fields.Mapping()
    number_of_days = fields.Method('get_number_of_days')
    change_history = fields.Method('get_change_history')

    @staticmethod
    def get_number_of_days(obj):
        return (obj.end_date - obj.start_date).days + 1

    @staticmethod
    def get_change_history(obj):
        change_history = CONFIG.HISTORY_LOG_SERVICE.fetch_all(request_id=obj.id, sort_='-created_at')

        if not change_history:
            return None
        return [
            {
                'value': json.loads(_.value),
                'created_at': _.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for _ in change_history
        ]


class RequestResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(RequestSerializer, many=True, attribute='instances')
