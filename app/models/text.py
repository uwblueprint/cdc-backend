from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Text

from . import Base


class Text(Base):
    __tablename__ = "text"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    next_text_id = Column(BigInteger, ForeignKey("text.id"), nullable=True)
    object_id = Column(BigInteger, nullable=False)
    columns = ["id", "content", "next_text_id", "object_id"]

    def __init__(self, content, next_text_id, object_id):
        self.content = content
        self.next_text_id = next_text_id
        self.object_id = object_id

    def as_dict(self):
        return {c: getattr(self, c) for c in self.columns}
