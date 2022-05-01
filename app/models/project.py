from sqlalchemy import Column, String, BIGINT
from configs.base import Base


class Project(Base):
    __tablename__ = 'project'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    name = Column(String)
    team_lead_id = Column(String)
