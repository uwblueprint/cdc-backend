from . import db


class Scene(db.Model):
    __tablename__ = "scene"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    object_ids = db.Column(db.Array(db.BigInteger), nullable=False)
    position = db.Column(db.Array(db.Float), nullable=False)
    scale = db.Column(db.Array(db.Float), nullable=False)
    rotation = db.Column(db.Array(db.Float), nullable=False)
    background_id = db.Column(db.BigInteger, db.ForeignKey("asset.id"), nullable=False)
