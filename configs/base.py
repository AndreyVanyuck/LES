import os

from flask import g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class ShardedConnection:

    def __init__(self):
        tenant_shard = os.environ.get('DB_HOST')
        tenant_user = os.environ.get('DB_USER')
        tenant_pass = os.environ.get('DB_PASSWORD')
        tenant_db = os.environ.get('DB_NAME')
        tenant_port = os.environ.get('DB_PORT', '5432')
        self.db = create_engine(
            f"postgresql+psycopg2://{tenant_user}:{tenant_pass}@{tenant_shard}:{tenant_port}/{tenant_db}",
            pool_size=10,
            max_overflow=2,
            pool_recycle=300,
            pool_pre_ping=True,
            pool_use_lifo=True
        )

    def create_session(self):
        session = sessionmaker(self.db, autocommit=True)
        session = session()
        return session

    @property
    def session(self):
        if getattr(g, 'session', None):
            return g.session
        else:
            g.session = self.create_session()
            return g.session


class BaseConfig:
    def __init__(self, *args, **kwargs):
        self.PG_DB = ShardedConnection().create_session()

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

    def setup_services(self):
        self._setup_postgres_services()

    def _setup_postgres_services(self):
        from app.services.user.user_service import UserService
        from app.services.department.department_service import DepartmentService
        from app.services.building.building_service import BuildingService
        from app.services.room.room_service import RoomService

        self.USER_SERVICE = UserService()
        self.DEPARTMENT_SERVICE = DepartmentService()
        self.ROOM_SERVICE = RoomService()
        self.BUILDING_SERVICE = BuildingService()
