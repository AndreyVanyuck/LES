from sqlalchemy import or_

from app.clients.postgres_client import PostgresClient
from app.models.user import User
from app.models.project import Project
from werkzeug.security import generate_password_hash


class UserService(PostgresClient):
    model = User

    def create(self, **kwargs):
        password = '123456'     # TODO generate password here

        kwargs['authorization_token'] = generate_password_hash(password)

        instance = super(UserService, self).create(**kwargs)

        return instance

    def _search_queryset(self, queryset, search_: str = None):
        return queryset.filter(
            or_(
                self.model.first_name.ilike(f"%{search_}%"),
                self.model.last_name.ilike(f"%{search_}%"),
                self.model.first_name_native.ilike(f"%{search_}%"),
                self.model.last_name_native.ilike(f"%{search_}%")
            )
        )

    def get_team_lead(self, project_id):
        team_lead_id_cte = self.pg_db.query(
            Project.team_lead_id.label('team_lead_id')
        ).select_from(
            Project
        ).filter(
            Project.id == project_id
        ).cte('team_lead_id_cte')

        return self.pg_db.query(
            self.model.id,
            self.model.first_name,
            self.model.last_name
        ).select_from(User).outerjoin(team_lead_id_cte, team_lead_id_cte.c.team_lead_id == self.model.id).filter(
            self.model.project_id == project_id
        ).all()