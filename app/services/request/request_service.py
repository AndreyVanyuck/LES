from app.clients.postgres_client import PostgresClient
from app.models.leave_request import LeaveRequest


class RequestService(PostgresClient):
    model = LeaveRequest

    def create(self, **kwargs):
        instance = self.model(**kwargs)

        self.pg_db.add(instance)
        self.pg_db.flush()

        return instance
