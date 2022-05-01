from app.utils.enums import RequestsStateEnum


class CreateRequestService:

    def __init__(self, request_service, user_service, project_service):
        self.request_service = request_service
        self.user_service = user_service
        self.project_service = project_service

    def create(self, **kwargs):
        user = self.user_service.fetch(id=kwargs.get('user_id'))

        state = self._generate_state_value(user)

        self.request_service.create(**kwargs)

    def _generate_state_value(self, user):
        payload = {
            'state': RequestsStateEnum.PENDING_APPROVAL.value,
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

        payload['current_to_approve'] = [{
            'id': _.id,
            'first_name': _.first_name,
            'last_name': _.last_name,
            'comment': None
        } for _ in personnel_officer]
        payload['next_to_register'] = payload['current_to_approve']

        team_lead_id = self.project_service.fetch(id=user.project_id).leam_lead_id
        team_lead = self.user_service.fetch(id=team_lead_id)
        manager = self.user_service.fetch(id=user.manager_id)

        payload['next_to_approve'].append({
            'id': team_lead.id,
            'first_name': team_lead.first_name,
            'last_name': team_lead.last_name,
            'comment': None
        })
        payload['next_to_approve'].append({
            'id': manager.id,
            'first_name': manager.first_name,
            'last_name': manager.last_name,
            'comment': None
        })

        return payload
