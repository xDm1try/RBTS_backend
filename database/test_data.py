import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer
from session import Base

class BatteryTest(Base):
    __tablename__ = "battery_tests"

    id = Column(Integer, primary_key=True, index=True)
    battery_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    temp_bat = Column(Float)
    temp_env = Column(Float)
    temp_load = Column(Float)
    bat_voltage = Column(Float)
    bat_current = Column(Float)
    load_voltage = Column(Float)
    load_current = Column(Float)
    load_duty = Column(Float)
    charge_status = Column(Boolean)
    const_current = Column(Float)
    const_voltage = Column(Float)
