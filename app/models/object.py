from sqlalchemy.dialects.postgresql import JSONB

from . import db


class Object(db.Model):
    __tablename__ = "object"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Array(db.Float), nullable=False)
    scale = db.Column(db.Array(db.Float), nullable=False)
    rotation = db.Column(db.Array(db.Float), nullable=False)
    asset_id = db.Column(db.BigInteger, db.ForeignKey("asset.id"), nullable=False)
    next_objects = db.Column(db.Array(db.BigInteger), nullable=True)
    text_id = db.Column(db.BigInteger, db.ForeignKey("text.id"), nullable=True)
    is_interactable = db.Column(db.Boolean, nullable=False)
    animations_json = db.Column(JSONB, nullable=False)
