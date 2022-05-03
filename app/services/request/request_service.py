from app.clients.postgres_client import PostgresClient
from app.models.leave_request import LeaveRequest


class RequestService(PostgresClient):
    model = LeaveRequest

