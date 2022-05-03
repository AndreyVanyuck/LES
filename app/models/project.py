from datetime import datetime

from sqlalchemy import Column, String, BIGINT, DateTime
from configs.base import Base


class Project(Base):
    __tablename__ = 'project'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    name = Column(String)
    team_lead_id = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

