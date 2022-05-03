from app.utils.enums import RequestsStateEnum


class UserRequestService:

    def __init__(self, request_service, user_service):
        self.request_service = request_service
        self.user_service = user_service

    def fetch_all(self, approver_id, user_id):
        all_request = self.request_service.fetch_all(user_id=user_id)
        require_approval = []
        require_approval_request_ids = []

        for request in all_request:
            approvers = request.state['current_to_approve']
            if request.state['state'] == RequestsStateEnum.APPROVED.value:
                approvers = request.state['current_to_register']
            for _ in approvers:
                if _['id'] == approver_id:
                    require_approval.append(request)
                    require_approval_request_ids.append(request.id)

        history_requests = [_ for _ in all_request if _.id not in require_approval_request_ids]

        return {'require_approval': require_approval, 'history_requests': history_requests}

    def declined(self, request_id, approver_id, comment):
        request = self.request_service.fetch(id=request_id)
        user = self.user_service.fetch(id=approver_id)

        new_state = request.state
        new_state['state'] = RequestsStateEnum.DECLINED.value
        new_state['declined'].append(
            {'id': user.id, 'comment': comment, 'first_name': user.first_name, 'last_name': user.last_name}
        )
        new_state['next_to_approve'].extend(new_state['current_to_approve'])
        new_state['current_to_approve'] = []

        request.state = new_state
        self.request_service.update(pk=request_id, **{'state': new_state})

        return request

    def approve(self, request_id, approver_id, comment):
        request = self.request_service.fetch(id=request_id)
        user = self.user_service.fetch(id=approver_id)

        new_state = request.state

        new_state['current_to_approve'] = [_ for _ in new_state['current_to_approve'] if _['id'] != approver_id]
        if not new_state['current_to_approve']:
            if new_state['next_to_approve']:
                new_state['current_to_approve'] = new_state['next_to_approve']
                new_state['next_to_approve'] = []
                new_state['approved'].append(
                    {'id': user.id, 'comment': comment, 'first_name': user.first_name, 'last_name': user.last_name}
                )
            elif new_state['next_to_register']:
                new_state['current_to_register'] = new_state['next_to_register']
                new_state['next_to_register'] = []
                new_state['approved'].append(
                    {'id': user.id, 'comment': comment, 'first_name': user.first_name, 'last_name': user.last_name}
                )
                new_state['state'] = RequestsStateEnum.APPROVED.value
            elif not new_state['next_to_register']:
                new_state['current_to_register'] = []
                new_state['registered'].append(
                    {'id': user.id, 'comment': comment, 'first_name': user.first_name, 'last_name': user.last_name}
                )
                new_state['state'] = RequestsStateEnum.APPROVED_AND_REGISTERED.value

        request.state = new_state
        self.request_service.update(pk=request_id, **{'state': new_state})

        return request
