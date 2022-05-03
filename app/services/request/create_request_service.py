from app.utils.enums import RequestsStateEnum, RequestTypeEnum


class CreateRequestService:

    def __init__(self, request_service, user_service, project_service):
        self.request_service = request_service
        self.user_service = user_service
        self.project_service = project_service

    def create(self, **kwargs):
        user = self.user_service.fetch(id=kwargs.get('user_id'))

        state = self.generate_state_value(user, kwargs.get('request_type'))

        request = self.request_service.create(**{'state': state}, **kwargs)

        return request

    def generate_state_value(self, user, request_type):
        payload = {
            'state': RequestsStateEnum.PENDING_CONFIRMATION.value if request_type == RequestTypeEnum.SICK_LEAVE.value else RequestsStateEnum.PENDING_APPROVAL.value,
            'current_to_approve': [],
            'next_to_approve': [],
            'next_to_register': [],
            'current_to_register': [],
            'notified': [],
            'declined': [],
            'approved': [],
            'registered': []
        }

        personnel_officer = self.user_service.fetch_all(is_personnel_officer=True)
        team_lead_id = self.project_service.fetch(id=user.project_id).team_lead_id
        team_lead = self.user_service.fetch(id=team_lead_id)
        manager = self.user_service.fetch(id=user.manager_id)

        if request_type == RequestTypeEnum.SICK_LEAVE.value:
            payload['notified'].append({
                'id': team_lead.id,
                'first_name': team_lead.first_name,
                'last_name': team_lead.last_name,
                'comment': None
            }) if team_lead else None
            payload['notified'].append({
                'id': manager.id,
                'first_name': manager.first_name,
                'last_name': manager.last_name,
                'comment': None
            }) if manager else None
            payload['current_to_register'] = [{
                'id': _.id,
                'first_name': _.first_name,
                'last_name': _.last_name,
                'comment': None
            } for _ in personnel_officer]

            return  payload

        payload['current_to_approve'] = [{
            'id': _.id,
            'first_name': _.first_name,
            'last_name': _.last_name,
            'comment': None
        } for _ in personnel_officer]
        payload['next_to_register'] = payload['current_to_approve']
        payload['next_to_approve'].append({
            'id': team_lead.id,
            'first_name': team_lead.first_name,
            'last_name': team_lead.last_name,
            'comment': None
        }) if team_lead else None
        payload['next_to_approve'].append({
            'id': manager.id,
            'first_name': manager.first_name,
            'last_name': manager.last_name,
            'comment': None
        }) if manager else None

        return payload
