from app.utils.validation_form import ValidationForm
from marshmallow import fields


class RoomsForm(ValidationForm):
    building_id = fields.Integer(required=False)