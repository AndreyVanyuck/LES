from app.utils.validation_form import ValidationForm
from marshmallow import fields, Schema
from app.main import CONFIG


class UserSerializer(ValidationForm):
    id = fields.Integer()
    title = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    first_name_native = fields.String()
    last_name_native = fields.String()
    middle_name_native = fields.String()
    room = fields.Method('get_room')
    building = fields.Method('get_building')
    email = fields.String()
    mobile_phone = fields.Integer()
    is_admin = fields.Boolean()
    created_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    updated_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    department = fields.Method('get_department')
    is_manager = fields.Boolean()
    manager = fields.Method('get_manager')
    hire_date = fields.DateTime(format='%Y-%m-%d')
    is_personnel_officer = fields.Boolean()
    status = fields.Method('get_status')

    def get_department(self, obj):
        departments = self.context.get('departments', [])

        department = next((_ for _ in departments if _.id == obj.department_id), None)

        return {
            'id': department.id,
            'name': department.name
        } if department else None

    @staticmethod
    def get_manager(obj):
        manager = CONFIG.USER_SERVICE.fetch(id=obj.manager_id)

        return {
            'id': manager.id,
            'first_name': manager.first_name,
            'last_name': manager.last_name
        } if manager else None

    def get_room(self, obj):
        if not obj.room_id:
            return 'N/A'

        rooms = self.context.get('rooms', [])

        room = next((_ for _ in rooms if _.id == obj.room_id), None)

        return {
            'id': room.id,
            'name': room.room
        }

    def get_building(self, obj):
        buildings = self.context.get('buildings', [])

        building = next((_ for _ in buildings if _.id == obj.building_id), None)

        return {
            'id': building.id,
            'address': building.address,
            'country': building.country
        } if building else None

    def get_status(self, obj):
        return 'active'


class VacationDaySerializer(ValidationForm):
    class _PeriodsSerializer(ValidationForm):
        start_date = fields.String()
        end_date = fields.String()
        vacation_norm = fields.Integer()
        days_earned = fields.Integer()
        days_left = fields.Integer()
        days_spent = fields.Integer()

    days_left = fields.Integer()
    periods = fields.Nested(_PeriodsSerializer, many=True, attribute='periods')


class UsersSerializer(UserSerializer):
    # department = fields.Integer(attribute='department_id')
    manager = fields.Integer(attribute='manager_id')


class UserResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(UserSerializer, many=True, attribute='instances')


class UserLoginSerializer(UserSerializer):
    authorization_token = fields.String()


class UserLoginResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(UserLoginSerializer, many=True, attribute='instances')


class UsersResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(UsersSerializer, many=True, attribute='instances')


class UserVacationDayResponseSerializer(Schema):
    total_count = fields.Int()
    data = fields.Nested(VacationDaySerializer, many=True, attribute='instances')
