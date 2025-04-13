from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from session import get_db
import schemas.battery_scheme as schemas
import repository.battery_crud as crud


router = APIRouter()


@router.post("/batteries/", response_model=schemas.Battery)
def create_battery(battery: schemas.BatteryCreate, db: Session = Depends(get_db)):
    db_battery = crud.get_battery_by_serial(db, serial_number=battery.serial_number)
    if db_battery:
        raise HTTPException(status_code=400, detail="Serial number already registered")
    return crud.create_battery(db=db, battery=battery)


@router.get("/batteries/", response_model=list[schemas.Battery])
def read_batteries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    batteries = crud.get_batteries(db, skip=skip, limit=limit)
    return batteries


@router.get("/batteries/{battery_id}", response_model=schemas.Battery)
def read_battery(battery_id: int, db: Session = Depends(get_db)):
    db_battery = crud.get_battery(db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery


@router.put("/batteries/{battery_id}", response_model=schemas.Battery)
def update_battery(battery_id: int, battery: schemas.BatteryCreate, db: Session = Depends(get_db)):
    db_battery = crud.get_battery(db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return crud.update_battery(db=db, battery_id=battery_id, battery=battery)


@router.delete("/batteries/{battery_id}", response_model=schemas.Battery)
def delete_battery(battery_id: int, db: Session = Depends(get_db)):
    db_battery = crud.delete_battery(db, battery_id=battery_id)
    if db_battery is None:
        raise HTTPException(status_code=404, detail="Battery not found")
    return db_battery
