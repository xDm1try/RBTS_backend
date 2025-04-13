import uvicorn
import asyncio
from fastapi import FastAPI
from utils import get_server_ip
from routers.battery import router as battery_router
from routers.announcements import router as announce_router




routes = (battery_router,
          announce_router,
          )

devices = []

ip = get_server_ip()
port = 21216


class RBTS_backend:
    def __init__(self, ip, port, routes: tuple):
        self.app = FastAPI()
        self.ip = ip
        self.port = port
        self.devices = []

        for r in routes:
            self.app.include_router(r)


rbts = RBTS_backend(ip, port, routes)


async def main():
    config = uvicorn.Config(rbts.app, host=ip, port=port)  # log_level="critical"
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
