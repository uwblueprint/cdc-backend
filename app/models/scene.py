from sqlalchemy import Array, BigInteger, Column, Float, ForeignKey, Integer, Text

from . import Base


class Scene(Base):
    __tablename__ = "scene"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    object_ids = Column(Array(BigInteger), nullable=False)
    position = Column(Array(Float), nullable=False)
    scale = Column(Array(Float), nullable=False)
    rotation = Column(Array(Float), nullable=False)
    background_id = Column(BigInteger, ForeignKey("asset.id"), nullable=False)

    def __init__(
        self, name, description, object_ids, position, scale, rotation, background_id
    ):
        self.name = name
        self.description = description
        self.object_ids = object_ids
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.background_id = background_id
