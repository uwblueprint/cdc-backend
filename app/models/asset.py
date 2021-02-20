from sqlalchemy import Column, Integer, Text

from . import Base


class Asset(Base):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    s3_key = Column(Text, nullable=False)
    obj_type = Column(Text, nullable=False)

    def __init__(self, name, s3_key, obj_type):
        self.name = name
        self.s3_key = s3_key
        self.obj_type = obj_type
