import uvicorn
import asyncio
from fastapi import FastAPI
from session import Base, engine
from utils import get_server_ip
from routers.battery import router as battery_router
from routers.announcements import router as announce_router
from routers.announcements import announce_handler


routes = (battery_router,
          announce_router,
          )

ip = get_server_ip()
ip = "0.0.0.0"
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
    asyncio.create_task(announce_handler.announce_handler_loop())
    config = uvicorn.Config(rbts.app, host=ip, port=port)  # log_level="critical"
    server = uvicorn.Server(config)
    Base.metadata.create_all(bind=engine)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
