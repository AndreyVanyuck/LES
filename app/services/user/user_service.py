from app.clients.postgres_client import PostgresClient
from app.models.user import User
from werkzeug.security import generate_password_hash


class UserService(PostgresClient):
    model = User

    def create(self, **kwargs):
        password = '123456'     # TODO generate password here

        kwargs['authorization_token'] = generate_password_hash(password)

        instance = super(UserService, self).create(**kwargs)

        return instance
