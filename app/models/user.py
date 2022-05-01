import datetime

from sqlalchemy import Column, String, Boolean, DateTime, BIGINT, Integer, ForeignKey

from configs.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    title = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    first_name_native = Column(String)
    last_name_native = Column(String)
    middle_name_native = Column(String)
    room_id = Column(Integer, ForeignKey('room.id'))
    building_id = Column(Integer, ForeignKey('building.id'))
    project_id = Column(Integer, ForeignKey('project.id'))
    email = Column(String)
    mobile_phone = Column(Integer)
    is_admin = Column(Boolean, default=False)
    is_manager = Column(Boolean, default=False)
    department_id = Column(Integer, ForeignKey('department.id'))
    authorization_token = Column(String)
    manager_id = Column(Integer)
    hire_date = Column(DateTime)
    is_personnel_officer = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
