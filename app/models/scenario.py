from sqlalchemy import Array, BigInteger, Boolean, Column, Integer, Text

from . import Base


class Scenario(Base):
    __tablename__ = "scenario"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    friendly_name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    scene_ids = Column(Array(BigInteger), nullable=False)
    is_published = Column(Boolean, nullable=False)
    is_previewable = Column(Boolean, nullable=False)
    publish_link = Column(Text, nullable=True)
    preview_link = Column(Text, nullable=True)
    expected_solve_time = Column(Text, nullable=False)
