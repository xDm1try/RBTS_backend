from pydantic import BaseModel


class ChargerSettings(BaseModel):
    const_current_mA: int
    const_volt_mV: int
    cut_off_current_mA: int
    temp_bat_limit: int


class ChargerStatus(BaseModel):
    const_current_mA: int
    const_volt_mV: int
    cut_off_current_mA: int
    input_type: str
    charge_status: str
    adc_battery_mV: int
    adc_bus_mV: int
    adc_current: int
    batfet_mode: bool
    termination_enabled: bool
    precharge_current: int
    low_battery_mV: int


class DeviceAnnounce(BaseModel):
    device_status: str
    device_name: str
    device_ip: str
    sd_free_mem: int


class StartSensors(BaseModel):
    test_id: str
    bat_id: str
    sleep_time: int


class TestData(BaseModel):
    temp_bat: int
    temp_env: int
    temp_load: int
    bat_voltage: int
    bat_current: int
    load_duty: int
    charge_status: str


class SetDuty:
    new_duty: int


class StartCharge:
    charge_settings: ChargerSettings
