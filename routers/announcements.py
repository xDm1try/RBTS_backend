import asyncio
from fastapi import APIRouter
from fastapi import Depends

from entities.device_announce import AnnounceHandler
from schemas.schemas import DeviceAnnounce
# from schemas.test_actions import DeviceTestRequest

from pprint import pprint as print


router = APIRouter()
announce_handler = AnnounceHandler()


@router.get("/device_announce_route")
async def handle_announce_request(device: DeviceAnnounce):
    print(device)
    announce_handler.add_device(new_device=device)
    return


@router.get("/get_device_list", response_model=list[DeviceAnnounce])
async def get_device_list():
    device_entities = announce_handler.get_devices()
    devices = []
    for dev in device_entities:
        devices.append(DeviceAnnounce(device_ip=dev.device_ip, device_name=dev.device_name,
                                      device_status=dev.device_status, sd_free_mem=dev.sd_free_mem))
    return devices


@router.get("/")
async def health():
    print("ALIVE")
    return {"status": "ok"}


# @router.get("/get_device_actions")
# async def get_device_list(test_request: DeviceTestRequest):
#     ...


# async def send_heartbeat(device_ip: str, device_port: int, message: str):
#     async with aiohttp.ClientSession() as session:

#         async with session.get(f"http://{device_ip}:{device_port}/", json=message) as response:
#             print(f"Status: {response.status}")
#             body = await response.text()
#             resp = json.loads(body)
#             hb_resp = HeartBeatResponse(**resp)
#             return hb_resp
