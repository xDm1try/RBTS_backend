from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ChargeParams(BaseModel):
    const_current_mA: int = Field(..., gt=0)
    const_volt_mV: int = Field(..., gt=0)
    cut_off_current_mA: int = Field(..., gt=0)
    duration: Optional[int] = Field(None, gt=0)
    temp_bat_limit: int = Field(..., gt=0)
    timeout: bool = Field(...)


class DischargeParams(BaseModel):
    dicharge_voltage_limit: int = Field(..., gt=0)
    discharge_current: int = Field(..., gt=0)
    duration: Optional[int] = Field(None, gt=0)
    start_duty: int = Field(..., ge=0, le=100)
    temp_bat_limit: int = Field(..., gt=0)
    timeout: bool = Field(...)


class WaitParams(BaseModel):
    duration: int = Field(..., gt=0)


class Action(BaseModel):
    type: str = Field(..., regex="^(Charge|Discharge|Wait)$")
    params: Dict = Field(...)


class DeviceTestRequest(BaseModel):
    actions: List[Action] = Field(..., min_items=1)
    device_ip: str = Field(..., regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    device_name: str = Field(..., min_length=1)
    filename: str = Field(..., min_length=1)
    polling_rate: int = Field(..., ge=1, le=60)
    sd_file: bool = Field(...)
