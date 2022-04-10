import datetime

from sqlalchemy import Column, String, Boolean, DateTime, BIGINT, Float, Integer


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
    department = Column(String)
    room = Column(Float, default=None)
    email = Column(String)
    mobile_phone = Column(Integer)
    is_admin = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
