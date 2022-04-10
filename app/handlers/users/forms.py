from app.utils.validation_form import ValidationForm
from marshmallow import fields, validate


class UserForm(ValidationForm):
    title = fields.String(validate=validate.OneOf(['mr, mrs']))
    first_name = fields.String()
    last_name = fields.String()
    first_name_native = fields.String()
    last_name_native = fields.String()
    middle_name_native = fields.String()
    department = fields.String()
    room = fields.Float()
    email = fields.String()
    mobile_phone = fields.Integer()
    is_admin = fields.Boolean(required=False, missing=False)

