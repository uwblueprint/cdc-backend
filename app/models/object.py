from sqlalchemy import Array, BigInteger, Boolean, Column, Float, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB

from . import Base


class Object(Base):
    __tablename__ = "object"
    id = Column(Integer, primary_key=True)
    position = Column(Array(Float), nullable=False)
    scale = Column(Array(Float), nullable=False)
    rotation = Column(Array(Float), nullable=False)
    asset_id = Column(BigInteger, ForeignKey("asset.id"), nullable=False)
    next_objects = Column(Array(BigInteger), nullable=True)
    text_id = Column(BigInteger, ForeignKey("text.id"), nullable=True)
    is_interactable = Column(Boolean, nullable=False)
    animations_json = Column(JSONB, nullable=False)
