from sqlalchemy import BigInteger, Boolean, Column, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY

from . import Base


class Scenario(Base):
    __tablename__ = "scenario"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    friendly_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    scene_ids = Column(ARRAY(BigInteger), nullable=False)
    is_published = Column(Boolean, nullable=False)
    is_previewable = Column(Boolean, nullable=False)
    publish_link = Column(Text, nullable=True)
    preview_link = Column(Text, nullable=True)
    expected_solve_time = Column(Text, nullable=False)

    def __init__(
        self,
        name,
        friendly_name,
        description,
        scene_ids,
        is_published,
        is_previewable,
        publish_link,
        preview_link,
        expected_solve_time,
    ):
        self.name = name
        self.friendly_name = friendly_name
        self.description = description
        self.scene_ids = scene_ids
        self.is_published = is_published
        self.is_previewable = is_previewable
        self.publish_link = publish_link
        self.preview_link = preview_link
        self.expected_solve_time = expected_solve_time
