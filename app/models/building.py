from sqlalchemy import Column, String, BIGINT
from configs.base import Base


class Building(Base):
    __tablename__ = 'building'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    address = Column(String)
    country = Column(String)
