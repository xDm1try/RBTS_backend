
import asyncio
import copy
import time
import aiohttp
from schemas.schemas import TestData
from schemas.test_actions import ChargeParams, DeviceTestRequest, DischargeParams, WaitParams


class TestRequestHandler:

    @classmethod
    async def handle_test_request(cls, test_request: DeviceTestRequest):

        if test_request.sd_file:
            cls.start_sd_writing(test_request)

        for action in test_request.actions:

            if action.type == "Charge":
                cls.handle_charge_action(test_request.device_ip, action, timeout=test_request.polling_rate)
            elif action.type == "Discharge":
                cls.handle_discharge_action(test_request.device_ip, action, timeout=test_request.polling_rate)
            elif action.type == "Wait":
                asyncio.sleep(action.duration, timeout=test_request.polling_rate)

        if test_request.sd_file:
            cls.stop_sd_writing(test_request)

    @classmethod
    async def start_sd_writing(cls, test_request: DeviceTestRequest):
        url = f"http://{test_request.device_ip}:21216/start_writing"
        params = {"timeout": test_request.polling_rate, "sd_file_name": test_request.filename}
        await cls.send_with_retry(url=url, data=params)        

    @classmethod
    async def stop_sd_writing(cls, test_request: DeviceTestRequest):
        url = f"http://{test_request.device_ip}:21216/stop_writing"
        await cls.send_with_retry(url=url)

    @classmethod
    async def handle_charge_action(cls, device_ip: str, action: ChargeParams, timeout: int):
        charge_url = f"http://{device_ip}:21216/start_charge"
        stop_url = f"http://{device_ip}:21216/stop_charge"
        get_data = f"http://{device_ip}:21216/get_sensors_data"

        params: ChargeParams = copy.deepcopy(action)
        del params.duration
        del params.timeout
        await cls.send_with_retry(charge_url, data=params)

        data: None | TestData = None

        while data is None or data.bat_current >= action.cut_off_current_mA:
            await asyncio.sleep(timeout)
            data = await cls.send_with_retry(get_data)
            print(data)

        await cls.send_with_retry(stop_url)

    @classmethod
    async def handle_discharge_action(cls, device_ip: str, action: DischargeParams, timeout: int):
        discharge_url = f"http://{device_ip}:21216/start_discharge"
        stop_url = f"http://{device_ip}:21216/stop_discharge"
        get_data = f"http://{device_ip}:21216/get_sensors_data"

        params: ChargeParams = copy.deepcopy(action)
        del params.duration
        del params.timeout
        await cls.send_with_retry(discharge_url, data=params)

        data: None | TestData = None

        while data is None or data.bat_voltage >= action.dicharge_voltage_limit:
            await asyncio.sleep(timeout)
            data = await cls.send_with_retry(get_data)
            print(data)

        await cls.send_with_retry(stop_url)

    @classmethod
    async def handle_wait_action(cls, device_ip, action: WaitParams, timeout: int):
        start = time.time()
        get_data = f"http://{device_ip}:21216/get_sensors_data"

        while time.time() - start < action.duration:
            await asyncio.sleep(timeout)
            data = await cls.send_with_retry(get_data)
            print(data)

    @classmethod
    async def send_with_retry(cls, url, data=None, max_retries=5, timeout=5) -> dict:
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    if data is None:
                        async with session.get(url, timeout=timeout) as response:
                            if response.status == 200:
                                return await response.json()
                            else:
                                print(f"Attempt {attempt + 1}: Status {response.status}")
                    else:
                        async with session.post(url, timeout=timeout, json=data) as response:
                            if response.status == 200:
                                return await response.json()
                            else:
                                print(f"Attempt {attempt + 1}: Status {response.status}")
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")

            if attempt < max_retries - 1:
                await asyncio.sleep(1 * (attempt + 1))

        raise Exception(f"All {max_retries} attempts failed")
