import os

from flask import g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class ShardedConnection:

    def __init__(self):
        self.create_session = sessionmaker(class_=ShardedSession)
        tenant_shards = os.environ.get('DB_HOST').split(",")
        shards = {}
        tenant_user = os.environ.get('DB_NAME')
        tenant_pass = os.environ.get('DB_NAME')
        tenant_db = os.environ.get('DB_NAME')
        tenant_port = os.environ.get('DB_PORT', '5432')
        for tenant_shard in tenant_shards:
            shards[tenant_shard] = create_engine(
                f"postgresql+psycopg2://{tenant_user}:{tenant_pass}@{tenant_shard}:{tenant_port}/{tenant_db}",
                pool_size=10,
                max_overflow=2,
                pool_recycle=300,
                pool_pre_ping=True,
                pool_use_lifo=True
            )

        self.create_session.configure(
            shards=shards
        )

        self.create_session.configure(
            shard_chooser=self.__shard_chooser,
            id_chooser=self.__id_chooser,
            query_chooser=self.__query_chooser
        )

    @staticmethod
    def __shard_chooser(mapper, instance, clause=None):
        if mapper and getattr(mapper.class_, '__bind_key__', None):
            return mapper.class_.__bind_key__
        return g.tenant_host

    @staticmethod
    def __id_chooser(query, ids):
        return ShardedConnection.__query_chooser(query)

    @staticmethod
    def __query_chooser(query):
        binds = set()
        for mapper in query._mapper_adapter_map.values():
            binds.add(ShardedConnection.__shard_chooser(*mapper))
            if len(binds) > 1:
                raise Exception("Unable to run a query across dbs: {', '.join(binds)}")
            return list(binds)
        return [g.tenant_host]

    @property
    def session(self):
        if getattr(g, 'session', None):
            return g.session
        else:
            g.session = self.create_session()
            return g.session


class BaseConfig:
    def __init__(self, *args, **kwargs):
        super(BaseConfig, self).__init__()

        self.PG_DB = ShardedConnection()

        self.UI_HOST = os.environ.get('UI_HOST')

        self.DB_HOST = os.environ.get('DB_HOST')
        self.DB_PORT = os.environ.get('DB_PORT', '5432')
        self.DB_NAME = os.environ.get('DB_NAME')
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME)

        self._setup_postgres_services()

    @staticmethod
    def setup_services():
        pass

    def _setup_postgres_services(self):
        from app.services.user.user_service import UserService
        self.USER_SERVICE = UserService()
