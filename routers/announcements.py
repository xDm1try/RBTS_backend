import asyncio
from fastapi import APIRouter
from fastapi import Depends

from entities.device_announce import AnnounceHandler
from entities.test_request_handler import TestRequestHandler
from schemas.schemas import DeviceAnnounce
from schemas.test_actions import DeviceTestRequest

from pprint import pprint as print


router = APIRouter()
announce_handler = AnnounceHandler()


@router.post("/device_announce_route")
async def handle_announce_request(device: DeviceAnnounce):
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


@router.post("/start_device_actions")
async def get_device_list(test_request: DeviceTestRequest):
    print(test_request.__dict__)
    loop = asyncio.get_event_loop()
    loop.create_task(TestRequestHandler.handle_test_request(test_request=test_request))