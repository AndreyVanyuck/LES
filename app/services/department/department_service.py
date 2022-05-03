from app.clients.postgres_client import PostgresClient
from app.models.department import Department


class DepartmentService(PostgresClient):
    model = Department
