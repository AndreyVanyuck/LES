import datetime

from sqlalchemy import Column, String, DateTime, BIGINT


from configs.base import Base


class Department(Base):
    __tablename__ = 'department'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    name = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

