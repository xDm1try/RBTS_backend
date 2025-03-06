import asyncio
from fastapi import APIRouter
from fastapi import Depends
import netifaces
from schemas.schemas import HeartBeatResponse
import socket
import time
import json
import aiohttp
from pprint import pprint as print
router = APIRouter()


@router.get("/device_announce")
async def device_announce(request: HeartBeatResponse):
    print(request)
    return


async def send_heartbeat(device_ip: str, device_port: int, message: str):
    async with aiohttp.ClientSession() as session:

        async with session.get(f"http://{device_ip}:{device_port}/", json=message) as response:
            print(f"Status: {response.status}")
            body = await response.text()
            resp = json.loads(body)
            hb_resp = HeartBeatResponse(**resp)
            return hb_resp
