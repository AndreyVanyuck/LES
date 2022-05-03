from datetime import datetime

from sqlalchemy import Column, String, BIGINT, DateTime
from configs.base import Base


class Building(Base):
    __tablename__ = 'building'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    address = Column(String)
    country = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

