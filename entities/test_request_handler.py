
import asyncio
import requests
import aiohttp
from schemas.test_actions import ChargeParams, DeviceTestRequest, DischargeParams, WaitParams


class TestRequestHandler:

    @classmethod
    async def handle_test_request(cls, test_request: DeviceTestRequest):

        if test_request.sd_file:
            cls.start_sd_writing(test_request)

        for action in test_request.actions:

            if action.type == "Charge":
                cls.handle_charge_action(test_request.device_ip, action)
            elif action.type == "Discharge":
                cls.handle_discharge_action(test_request.device_ip, action)
            elif action.type == "Wait":
                asyncio.sleep(action.duration)

        if test_request.sd_file:
            cls.stop_sd_writing(test_request)

    @classmethod
    async def start_sd_writing(cls, test_request: DeviceTestRequest):
        url = f"http://{test_request.device_ip}:21216/start_writing"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)

    @classmethod
    async def stop_sd_writing(cls, test_request: DeviceTestRequest):
        url = f"http://{test_request.device_ip}:21216/stop_writing"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)

    @classmethod
    async def handle_charge_action(cls, device_ip: str, action: ChargeParams):
        charge_url = f"http://{device_ip}:21216/start_charge"
        stop_url = f"http://{device_ip}:21216/stop_charge"
        # TODO

    @classmethod
    async def handle_discharge_action(cls, device_ip: str, action: DischargeParams):
        charge_url = f"http://{device_ip}:21216/start_charge"
        stop_url = f"http://{device_ip}:21216/stop_charge"
        # TODO

    @classmethod
    async def handle_wait_action(cls, action: WaitParams):
        await asyncio.sleep(action.duration)

    async def writer_db_loop(cls, device_ip: str):
        url = f"http://{test_request.device_ip}:21216/get_sensors_data"
        while True:
            async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print(data)