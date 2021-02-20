from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class Statistics(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True)
    scenario_id = Column(BigInteger, ForeignKey("scenario.id"), nullable=True)
    scene_id = Column(BigInteger, ForeignKey("scene.id"), nullable=True)
    object_id = Column(BigInteger, ForeignKey("object.id"), nullable=True)
    stats = Column(JSONB, nullable=False)
