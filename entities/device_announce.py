import asyncio
import copy
import time
from schemas.schemas import DeviceAnnounce


class DeviceAnnounceEntity:
    def __init__(self, device_announce_scheme: DeviceAnnounce):
        self.device_name = device_announce_scheme.device_name
        self.device_ip = device_announce_scheme.device_ip
        self.device_status = device_announce_scheme.device_status
        self.sd_free_mem = device_announce_scheme.sd_free_mem
        self.announce_time = time.time()


class AnnounceHandler:
    def __init__(self):
        self.detected_devices: list[DeviceAnnounceEntity] = []

    def add_device(self, new_device: DeviceAnnounce) -> None:
        for device in self.detected_devices:
            if device.device_name == new_device.device_name and device.device_ip == new_device.device_ip:
                device.device_status = new_device.device_status
                device.announce_time = time.time()
                device.device_status = new_device.device_status
                device.sd_free_mem = new_device.sd_free_mem
                return
        self.detected_devices.append(DeviceAnnounceEntity(new_device))

    def update(self) -> None:
        current_time: int = time.time()
        self.detected_devices = [device for device in self.detected_devices if device.announce_time > current_time - 600]
        self.detected_devices.sort(key=lambda x: x.device_name)

    def get_devices(self):
        return copy.deepcopy(self.detected_devices)

    async def announce_handler_loop(self):
        print("Announce loop started")
        while True:
            await asyncio.sleep(1)
            self.update()
