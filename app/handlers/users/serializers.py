from datetime import datetime

from app.utils.enums import RequestsStateEnum, UserPicture
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
    is_absent = fields.Method('get_is_absent')
    avatar = fields.Method('get_avatar')

    @staticmethod
    def get_avatar(obj):
        return UserPicture.women.value

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
        } if room else None

    def get_building(self, obj):
        buildings = self.context.get('buildings', [])

        building = next((_ for _ in buildings if _.id == obj.building_id), None)

        return {
            'id': building.id,
            'address': building.address,
            'country': building.country
        } if building else None

    @staticmethod
    def get_status(obj):
        return 'active'

    @staticmethod
    def get_is_absent(obj):
        now = datetime.utcnow().strftime('%Y-%m-%d')
        requests = CONFIG.REQUEST_SERVICE.fetch_all(user_id=obj.id, gte_={'end_date': now}, lte_={'start_date': now})

        requests = [
            _ for _ in requests
            if _.state['state'] in [RequestsStateEnum.APPROVED.value, RequestsStateEnum.APPROVED_AND_REGISTERED.value]
        ]
        return {'end_date': requests[0].end_date.strftime('%Y-%m-%d'), 'request_type': requests[0].request_type} if requests else None


class VacationDaySerializer(ValidationForm):
    class _PeriodsSerializer(ValidationForm):
        start_date = fields.String()
        end_date = fields.String()
        vacation_norm = fields.Integer()
        days_earned = fields.Integer()
        days_left = fields.Integer()
        days_spent = fields.Integer()
        sick_leave_days = fields.Integer()
        own_expense_days = fields.Integer()

    available_vacation_days = fields.Integer()
    vacation_norm = fields.Integer()
    sick_leave_days = fields.Integer()
    own_expense_days = fields.Integer()
    periods = fields.Nested(_PeriodsSerializer, many=True, attribute='periods')


class UsersSerializer(UserSerializer):
    # department = fields.Integer(attribute='department_id')
    manager = fields.Integer(attribute='manager_id')
    project = fields.Method('get_project')
    leave_dates = fields.Method('get_leave_dates')

    def get_project(self, obj):
        projects = self.context.get('projects', [])
        team_leads = self.context.get('team_leads', [])

        project = next((_ for _ in projects if _.id == obj.project_id), None)
        team_lead = next((_ for _ in team_leads if _.id == project.team_lead_id), None) if project else None

        return {
            'id': project.id,
            'name': project.name,
            'team_lead': {'id': team_lead.id, 'first_name': team_lead.first_name, 'last_name': team_lead.last_name}
        } if project else None

    @staticmethod
    def get_leave_dates(obj):
        days = CONFIG.VACATION_DAY_CALCULATION_SERVICE.get_remained_days(user_id=obj.id)
        return days


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
