from sqlalchemy import Column, ForeignKey, Integer, Text, Date, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="todos")
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    date = Column(Date, nullable=False)
