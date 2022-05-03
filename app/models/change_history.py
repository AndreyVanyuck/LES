from datetime import datetime

from sqlalchemy import Column, BIGINT, Integer, Text, DateTime
from configs.base import Base


class HistoryLog(Base):
    __tablename__ = 'change_history'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    request_id = Column(Integer)
    value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

