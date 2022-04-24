from sqlalchemy import Column, String, BIGINT, Integer, ForeignKey
from configs.base import Base


class Room(Base):
    __tablename__ = 'room'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    room = Column(Integer)
    building_id = Column(Integer, ForeignKey('building.id'))
