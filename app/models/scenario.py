from . import db


class Scenario(db.Model):
    __tablename__ = "scenario"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    friendly_name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    scene_ids = db.Column(db.Array(db.BigInteger), nullable=False)
    is_published = db.Column(db.Boolean, nullable=False)
    is_previewable = db.Column(db.Boolean, nullable=False)
    publish_link = db.Column(db.Text, nullable=True)
    preview_link = db.Column(db.Text, nullable=True)
    expected_solve_time = db.Column(db.Text, nullable=False)
