from app.clients.postgres_client import PostgresClient
from app.models.project import Project


class ProjectService(PostgresClient):
    model = Project
