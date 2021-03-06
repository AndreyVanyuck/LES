import datetime

from sqlalchemy import Column, String, BIGINT, Integer, ForeignKey, DateTime
from configs.base import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    comment = Column(String)
    request_id = Column(Integer, ForeignKey('leave_request.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



