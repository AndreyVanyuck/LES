import json

from app.utils.enums import RequestsStateEnum


class UpdateRequestService:

    def __init__(self, request_service, history_log_service, user_service, create_request_service):
        self.request_service = request_service
        self.history_log_service = history_log_service
        self.user_service = user_service
        self.create_request_service = create_request_service

    def update(self, pk, user_id, **kwargs):
        old_request = self.request_service.fetch(id=pk)

        value = self._generate_log_value(old_request)

        self.history_log_service.create(**{'request_id': old_request.id, 'value': json.dumps(value)})

        user = self.user_service.fetch(id=user_id)
        state = self.create_request_service.generate_state_value(user)

        self.request_service.update(pk=pk, **{'state': state}, **kwargs)
        new_request = self.request_service.fetch(id=pk)

        return new_request

    @staticmethod
    def _generate_log_value(old_request):
        return {
            'start_date': old_request.start_date.strftime('%Y-%m-%d'),
            'end_date': old_request.end_date.strftime('%Y-%m-%d'),
            'comment': old_request.comment
        }

    def cancel_request(self, pk):
        old_request = self.request_service.fetch(id=pk)

        new_state = old_request.state
        new_state['state'] = RequestsStateEnum.CANCELED.value

        self.request_service.update(pk=pk, **{'state': new_state})

        new_request = self.request_service.fetch(id=pk)

        return new_request
