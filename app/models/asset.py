from . import db


class Asset(db.Model):
    __tablename__ = "asset"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    s3_key = db.Column(db.Text, nullable=False)
    obj_type = db.Column(db.Text, nullable=False)
