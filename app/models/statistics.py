from sqlalchemy.dialects.postgresql import JSONB

from . import db


class Statistics(db.Model):
    __tablename__ = "statistics"
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.BigInteger, db.ForeignKey("scenario.id"), nullable=True)
    scene_id = db.Column(db.BigInteger, db.ForeignKey("scene.id"), nullable=True)
    object_id = db.Column(db.BigInteger, db.ForeignKey("object.id"), nullable=True)
    stats = db.Column(JSONB, nullable=False)
