from pydantic import BaseModel


class BatteryBase(BaseModel):
    serial_number: str
    capacity: int
    comments: str | None = None


class BatteryCreate(BatteryBase):
    pass


class Battery(BatteryBase):
    id: int

    class Config:
        from_attributes = True
