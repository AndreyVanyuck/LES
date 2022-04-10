import datetime

from sqlalchemy import Column, String, Boolean, DateTime, BIGINT, func, select, case, and_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from configs.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BIGINT, autoincrement=True, primary_key=True)
    name = Column(String())
    surname = Column(String())

    is_archived = Column(Boolean(), default=False)
    labels = Column(ARRAY(String), default=[])
    created_at = Column(DateTime(), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.datetime.utcnow)
    users_favorite = Column(ARRAY(String), default=[])

    campaigns = relationship('Campaign', secondary='campaign_w_ad_group_mapping', lazy='select')
    creatives = relationship('Creative', secondary='creative_w_ad_group_mapping', lazy='select')

