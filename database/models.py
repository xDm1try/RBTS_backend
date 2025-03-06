from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()


class ChargerStatus(Base):
    __tablename__ = "charger_status"

    id = Column(Integer, primary_key=True, index=True)

    const_current_mA = Column(Integer)
    const_volt_mV = Column(Integer)
    cut_off_current_mA = Column(Integer)
    input_type = Column(String)
    charge_status = Column(String)
    adc_battery_mV = Column(Integer)
    adc_bus_mV = Column(Integer)
    adc_current = Column(Integer)
    batfet_mode = Column(Boolean)
    termination_enabled = Column(Boolean)
    precharge_current = Column(Integer)
    low_battery_mV = Column(Integer)

    heartbeat_response_id = Column(Integer, ForeignKey("heartbeat_response.id"))

    heartbeat_response = relationship("HeartBeatResponse", back_populates="charger_status")


class HeartBeatResponse(Base):
    __tablename__ = "heartbeat_response"

    id = Column(Integer, primary_key=True, index=True)

    device_status = Column(String)
    device_name = Column(String)
    device_ip = Column(String)

    charger_status_id = Column(Integer, ForeignKey("charger_status.id"))

    charger_status = relationship("ChargerStatus", back_populates="heartbeat_response")
