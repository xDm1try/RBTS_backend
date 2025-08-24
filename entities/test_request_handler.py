
import asyncio
import copy
import time
import aiohttp
from schemas.schemas import TestData
from schemas.test_actions import Action, ChargeParams, DeviceTestRequest, DischargeParams, StartWritingParams, WaitParams


class TestRequestHandler:

    @classmethod
    async def handle_test_request(cls, test_request: DeviceTestRequest):

        if test_request.sd_file:
            print("start writing")
            await cls.start_sd_writing(test_request)

        for action in test_request.actions:

            if action.type == "Charge":
                print(f"action={action=}")
                print("start charging")
                await cls.handle_charge_action(test_request.device_ip, action, timeout=test_request.polling_rate)
            elif action.type == "Discharge":
                print("start discharging")
                await cls.handle_discharge_action(test_request.device_ip, action, timeout=test_request.polling_rate)
            elif action.type == "Wait":
                print("start waiting")
                await cls.handle_wait_action(test_request.device_ip, action, timeout=test_request.polling_rate)

        if test_request.sd_file:
            print("stop writing")
            await cls.stop_sd_writing(test_request)

    @classmethod
    async def start_sd_writing(cls, test_request: DeviceTestRequest):
        url = f"http://{test_request.device_ip}:21216/start_writing"
        params = StartWritingParams(frequency=test_request.polling_rate, sd_file_name=test_request.filename)
        await cls.send_with_retry(url=url, data=params)

    @classmethod
    async def stop_sd_writing(cls, test_request: DeviceTestRequest):
        url = f"http://{test_request.device_ip}:21216/stop_writing"
        await cls.send_with_retry(url=url)

    @classmethod
    async def handle_charge_action(cls, device_ip: str, action: Action, timeout: int):
        charge_url = f"http://{device_ip}:21216/start_charge"
        stop_url = f"http://{device_ip}:21216/stop_charge"
        get_data = f"http://{device_ip}:21216/get_sensors_data"

        parameters: ChargeParams = copy.deepcopy(action.params)
        params: ChargeParams = copy.deepcopy(action.params)
        del params.duration
        del params.timeout
        await cls.send_with_retry(charge_url, data=params)

        for i in range(5):
            await asyncio.sleep(timeout)

        data: None | TestData = None

        if parameters.timeout is False:
            while data is None or data.get("bat_current") >= params.cut_off_current_mA:
                await asyncio.sleep(timeout)
                data = await cls.send_with_retry(get_data)
                print(data)
        else:
            for i in range(parameters.duration):
                await asyncio.sleep(timeout)
                data = await cls.send_with_retry(get_data)
                print(data)

        await cls.send_with_retry(stop_url)

    @classmethod
    async def handle_discharge_action(cls, device_ip: str, action: Action, timeout: int):
        discharge_url = f"http://{device_ip}:21216/start_discharge"
        stop_url = f"http://{device_ip}:21216/stop_discharge"
        get_data = f"http://{device_ip}:21216/get_sensors_data"
        parameters: DischargeParams = copy.deepcopy(action.params)
        params: DischargeParams = copy.deepcopy(action.params)
        del params.duration
        del params.timeout
        await cls.send_with_retry(discharge_url, data=params)

        for i in range(5):
            await asyncio.sleep(timeout)
            data = await cls.send_with_retry(get_data)
            print(data)
        data: None | TestData = None

        if parameters.timeout is False:
            while data is None or data.get("bat_voltage") >= params.dicharge_voltage_limit:
                await asyncio.sleep(timeout)
                data = await cls.send_with_retry(get_data)
                print(data)
        else:
            for i in range(parameters.duration):
                await asyncio.sleep(timeout)
                data = await cls.send_with_retry(get_data)
                print(data)

        await cls.send_with_retry(stop_url)

    @classmethod
    async def handle_wait_action(cls, device_ip, action: WaitParams, timeout: int):
        start = time.time()
        get_data = f"http://{device_ip}:21216/get_sensors_data"
        params: DischargeParams = copy.deepcopy(action.params)

        while time.time() - start < params.duration:
            await asyncio.sleep(timeout)
            data = await cls.send_with_retry(get_data)
            print(data)

    @classmethod
    async def send_with_retry(cls, url, data=None, max_retries=5, timeout=10) -> dict:
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    if data is None:
                        async with session.get(url, timeout=timeout) as response:
                            if response.status >= 200 and response.status < 300:
                                return await response.json()
                            else:
                                print(f"Attempt {attempt + 1}: Status {response.status}")
                    else:
                        print(f"SENDING: {url=}\n{data=}")
                        print(f"data json = {data.__dict__}")
                        async with session.get(url, timeout=timeout, json=data.__dict__) as response:
                            if response.status >= 200 and response.status < 300:
                                return await response.json()
                            else:
                                print(f"Attempt {attempt + 1}: Status {response.status}")
            except Exception as e:
                print(f"\n\nEXCEPTION = {e=}\n\n")

        raise Exception(f"All {max_retries} attempts failed")
