from . import db


class Text(db.Model):
    __tablename__ = "text"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    next_text_id = db.Column(db.BigInteger, db.ForeignKey("text.id"), nullable=True)
    object_id = db.Column(db.BigInteger, nullable=False)
