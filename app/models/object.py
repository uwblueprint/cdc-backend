from sqlalchemy import BigInteger, Boolean, Column, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from . import Base


class Object(Base):
    __tablename__ = "object"
    id = Column(Integer, primary_key=True)
    position = Column(ARRAY(Float), nullable=False)
    scale = Column(ARRAY(Float), nullable=False)
    rotation = Column(ARRAY(Float), nullable=False)
    asset_id = Column(BigInteger, ForeignKey("asset.id"), nullable=False)
    next_objects = Column(ARRAY(JSONB), nullable=True)
    text_id = Column(BigInteger, ForeignKey("text.id"), nullable=True)
    is_interactable = Column(Boolean, nullable=False)
    animations_json = Column(JSONB, nullable=False)

    def __init__(
        self,
        position,
        scale,
        rotation,
        asset_id,
        next_objects,
        text_id,
        is_interactable,
        animations_json,
    ):
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.asset_id = asset_id
        self.next_objects = next_objects
        self.text_id = text_id
        self.is_interactable = is_interactable
        self.animations_json = animations_json
