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
        tenant_shard = 'ec2-3-230-122-20.compute-1.amazonaws.com'  # os.environ.get('DB_HOST')
        tenant_port = '5432'  # os.environ.get('DB_PORT', '5432')
        tenant_db = 'd57f4rbl8dvo8p'  # os.environ.get('DB_NAME')
        tenant_user = 'gjktymcqonvqpe'  # os.environ.get('DB_USER')
        tenant_pass = 'd10f6705edc6e885cd6caab4780c926c33322fd4ba3504971ec099f68c6a2d23'  # os.environ.get('DB_PASSWORD')

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

        self.DB_HOST = 'ec2-3-230-122-20.compute-1.amazonaws.com' #os.environ.get('DB_HOST')
        self.DB_PORT = '5432' #os.environ.get('DB_PORT', '5432')
        self.DB_NAME = 'd57f4rbl8dvo8p' #os.environ.get('DB_NAME')
        self.DB_USER = 'gjktymcqonvqpe' #os.environ.get('DB_USER')
        self.DB_PASSWORD = 'd10f6705edc6e885cd6caab4780c926c33322fd4ba3504971ec099f68c6a2d23' #os.environ.get('DB_PASSWORD')
        self.SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME)

    def setup_services(self):
        self._setup_postgres_services()
        self._setup_vacation_day_calculation_services()

    def _setup_postgres_services(self):
        from app.services.user.user_service import UserService
        from app.services.department.department_service import DepartmentService
        from app.services.building.building_service import BuildingService
        from app.services.room.room_service import RoomService
        from app.services.request.request_service import RequestService
        from app.services.project.project_service import ProjectService
        from app.services.change_history.change_history_service import HistoryLogService

        self.USER_SERVICE = UserService()
        self.DEPARTMENT_SERVICE = DepartmentService()
        self.ROOM_SERVICE = RoomService()
        self.BUILDING_SERVICE = BuildingService()
        self.REQUEST_SERVICE = RequestService()
        self.PROJECT_SERVICE = ProjectService()
        self.HISTORY_LOG_SERVICE = HistoryLogService()

    def _setup_vacation_day_calculation_services(self):
        from app.services.vacation.vacation_day_calculation_service import VacationDayCalculationService
        from app.services.request.create_request_service import CreateRequestService
        from app.services.request.update_request_service import UpdateRequestService
        from app.services.user.user_list_service import UserListService
        from app.services.request.user_request_service import UserRequestService

        self.VACATION_DAY_CALCULATION_SERVICE = VacationDayCalculationService(
            user_service=self.USER_SERVICE,
            request_service=self.REQUEST_SERVICE
        )

        self.CREATE_REQUEST_SERVICE = CreateRequestService(
            request_service=self.REQUEST_SERVICE,
            user_service=self.USER_SERVICE,
            project_service=self.PROJECT_SERVICE
        )
        self.UPDATE_REQUEST_SERVICE = UpdateRequestService(
            request_service=self.REQUEST_SERVICE,
            user_service=self.USER_SERVICE,
            history_log_service=self.HISTORY_LOG_SERVICE,
            create_request_service=self.CREATE_REQUEST_SERVICE
        )

        self.USER_LIST_SERVICE = UserListService(
            user_service=self.USER_SERVICE,
            project_service=self.PROJECT_SERVICE,
            request_service=self.REQUEST_SERVICE
        )

        self.USER_REQUEST_SERVICE = UserRequestService(
            request_service=self.REQUEST_SERVICE,
            user_service=self.USER_SERVICE
        )
