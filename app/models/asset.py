from models.base import BaseModel
from sqlalchemy import Column, Integer, Text


class Asset(BaseModel):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    s3_key = Column(Text, nullable=False)
    obj_type = Column(Text, nullable=False)
    screenshot_url = Column(Text, nullable=False, default="")
    columns = ["id", "name", "s3_key", "obj_type", "screenshot_url"]
