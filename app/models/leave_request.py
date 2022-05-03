import datetime

from sqlalchemy import Column, String, BIGINT, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from configs.base import Base


class LeaveRequest(Base):
    __tablename__ = 'leave_request'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    request_type = Column(String)
    comment = Column(String)
    state = Column(JSONB, default=[])

