from . import Base


class BaseModel(Base):
    __abstract__ = True
    # Child classes need to define their own columns
    columns = []

    def as_dict(self):
        return {c: getattr(self, c) for c in self.columns}
