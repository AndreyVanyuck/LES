from datetime import datetime

from sqlalchemy import Column, String, BIGINT, Integer, ForeignKey, DateTime
from configs.base import Base


class Room(Base):
    __tablename__ = 'room'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    room = Column(Integer)
    building_id = Column(Integer, ForeignKey('building.id'))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

