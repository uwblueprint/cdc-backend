from models.base import BaseModel
from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB


class Statistics(BaseModel):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True)
    scenario_id = Column(BigInteger, ForeignKey("scenario.id"), nullable=True)
    scene_id = Column(BigInteger, ForeignKey("scene.id"), nullable=True)
    object_id = Column(BigInteger, ForeignKey("object.id"), nullable=True)
    stats = Column(JSONB, nullable=False)
    columns = ["id", "scenario_id", "scene_id", "object_id", "stats"]

    def __init__(self, scenario_id, scene_id, object_id, stats):
        self.scenario_id = scenario_id
        self.scene_id = scene_id
        self.object_id = object_id
        self.stats = stats
