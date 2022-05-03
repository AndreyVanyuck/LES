from app.utils.enums import RequestTypeEnum
from app.utils.validation_form import ValidationForm
from marshmallow import fields, validate


class RequestCreateForm(ValidationForm):
    request_type = fields.String(required=True, validate=validate.OneOf(RequestTypeEnum.values()))
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    comment = fields.String(allow_none=True)


class RequestsListFetchForm(ValidationForm):
    user_id = fields.String(required=False)
#     search_ = fields.String(required=False, data_key='search')
#     email = fields.String(required=False)
#
#     building_id = fields.Integer(required=False)
#     room_id = fields.Integer(required=False)
#     department_id = fields.Integer(required=False)
#     is_manager = fields.Boolean(required=False)
#     sort_ = fields.String(
#         required=False,
#         default='id',
#         data_key='sort'
#     )


class RequestUpdateForm(ValidationForm):
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    comment = fields.String(allow_none=True)
