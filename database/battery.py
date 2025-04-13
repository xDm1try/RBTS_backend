from sqlalchemy import Column, Integer, String, Text

from session import Base


class Battery(Base):
    __tablename__ = "batteries"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String, unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    comments = Column(Text, nullable=True)
