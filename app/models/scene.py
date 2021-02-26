from models.base import BaseModel
from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY


class Scene(BaseModel):
    __tablename__ = "scene"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False, default="")
    object_ids = Column(ARRAY(BigInteger), nullable=False, default=[])
    position = Column(ARRAY(Float), nullable=False, default=[])
    scale = Column(ARRAY(Float), nullable=False, default=[])
    rotation = Column(ARRAY(Float), nullable=False, default=[])
    background_id = Column(BigInteger, ForeignKey("asset.id"), nullable=False)
    columns = [
        "id",
        "name",
        "description",
        "object_ids",
        "position",
        "scale",
        "rotation",
        "background_id",
    ]
