from app.clients.postgres_client import PostgresClient
from app.models.user import User


class UserService(PostgresClient):
    model = User
