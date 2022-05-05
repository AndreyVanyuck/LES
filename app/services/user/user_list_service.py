from datetime import datetime

from app.utils.enums import RequestsStateEnum


class UserListService:

    def __init__(self, user_service, project_service, request_service):
        self.user_service = user_service
        self.project_service = project_service
        self.request_service = request_service

    def fetch_all(self, user_id,  **kwargs):
        grouping = kwargs.get('grouping')
        if kwargs.get('grouping'):
            kwargs.pop('grouping')

        if not grouping:
            return self.user_service.fetch_all(**kwargs)

        user = self.user_service.fetch(id=user_id)

        if user.is_manager:
            project = self.project_service.fetch(team_lead_id=user.id)

            users = self.user_service.fetch_all(
                **kwargs,
                in_or_={'manager_id': [user.id], 'project_id': [project.id] if project else None},
                not_={'id': user.id},
                sort_='last_name'
            )

        if user.is_personnel_officer:
            users = self.user_service.fetch_all(
                **kwargs,
                not_={'id': user.id},
                sort_='last_name'
            )

        if grouping == 'all':
            return users

        now = datetime.utcnow().strftime('%Y-%m-%d')

        requests = self.request_service.fetch_all(
            gte_={'end_date': now},
            lte_={'start_date': now},
            in_and_={'user_id': list({_.id for _ in users})}
        )

        user_ids = []
        if grouping == 'on_a_leave':
            user_ids = [_.user_id for _ in requests if _.state['state'] in [RequestsStateEnum.APPROVED.value, RequestsStateEnum.APPROVED_AND_REGISTERED.value]]

        if grouping == 'require_approval':
            for request in requests:
                if user.is_manager:
                    approvers = request.state['current_to_approve']
                elif user.is_personnel_officer:
                    approvers = request.state['current_to_approve']
                    approvers.extend(request.state['current_to_register'])
                for _ in approvers:
                    if _['id'] == user_id:
                        user_ids.append(request.user_id)

        users = [_ for _ in users if _.id in user_ids]

        return users
