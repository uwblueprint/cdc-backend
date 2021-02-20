from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Text

from . import Base


class Text(Base):
    __tablename__ = "text"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    next_text_id = Column(BigInteger, ForeignKey("text.id"), nullable=True)
    object_id = Column(BigInteger, nullable=False)
