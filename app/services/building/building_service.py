from app.clients.postgres_client import PostgresClient
from app.models.building import Building


class BuildingService(PostgresClient):
    model = Building
