from fastapi import APIRouter
from fastapi import Depends


router = APIRouter()


@router.get("/all_devices")
async def read_users():
    return ["dev1"]
