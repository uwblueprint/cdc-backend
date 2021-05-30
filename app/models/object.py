from models.base import BaseModel
from sqlalchemy import BigInteger, Boolean, Column, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB


class Object(BaseModel):
    __tablename__ = "object"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    position = Column(ARRAY(Float), nullable=False)
    scale = Column(ARRAY(Float), nullable=False)
    rotation = Column(ARRAY(Float), nullable=False)
    asset_id = Column(
        BigInteger, ForeignKey("asset.id", ondelete="CASCADE"), nullable=False
    )
    next_objects = Column(ARRAY(JSONB), nullable=True)
    texts = Column(ARRAY(Text), nullable=False, default=[""])
    is_interactable = Column(Boolean, nullable=False)
    animations_json = Column(JSONB, nullable=False, default={})
    columns = [
        "id",
        "name",
        "position",
        "scale",
        "rotation",
        "asset_id",
        "next_objects",
        "texts",
        "is_interactable",
        "animations_json",
    ]
