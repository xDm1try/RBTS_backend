import json
import uvicorn
import asyncio
from fastapi import FastAPI
from utils import get_broadcast_address, get_addreses, get_server_ip
from routers.announcements import router as announce_router, send_announce_loop
from routers.devices import router as device_router
from routers.frontend import router as frontend_router
from schemas.schemas import AnnouncementModel

routes = (announce_router, device_router, frontend_router)

devices = []

ip = get_server_ip()
port = 61212


class RBTS_backend:
    def __init__(self, ip, port, routes: tuple):
        self.app = FastAPI()
        self.ip = ip
        self.port = port
        self.devices = []

        for r in routes:
            self.app.include_router(r)


app = RBTS_backend(ip, port, routes)


async def main():
    config = uvicorn.Config(app, host=ip, port=port)  # log_level="critical"
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
