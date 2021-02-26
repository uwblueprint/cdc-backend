from models.base import BaseModel
from sqlalchemy import BigInteger, Boolean, Column, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY


class Scenario(BaseModel):
    __tablename__ = "scenario"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    friendly_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    scene_ids = Column(ARRAY(BigInteger), nullable=False, default=[])
    is_published = Column(Boolean, nullable=False, default=False)
    is_previewable = Column(Boolean, nullable=False, default=False)
    publish_link = Column(Text, nullable=True)
    preview_link = Column(Text, nullable=True)
    expected_solve_time = Column(Text, nullable=False, default="")
    columns = [
        "id",
        "name",
        "friendly_name",
        "description",
        "scene_ids",
        "is_published",
        "is_previewable",
        "publish_link",
        "preview_link",
        "expected_solve_time",
    ]
