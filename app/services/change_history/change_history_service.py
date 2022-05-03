from app.clients.postgres_client import PostgresClient
from app.models.change_history import HistoryLog


class HistoryLogService(PostgresClient):
    model = HistoryLog
