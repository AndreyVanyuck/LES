from marshmallow import Schema, ValidationError

from app.utils.custom_exceptions import BadRequestAPIException


class ValidationForm(Schema):

    def load(self, *args, **kwargs):
        try:
            return super().load(*args, **kwargs)
        except ValidationError as e:
            raise BadRequestAPIException(payload=e.messages)
