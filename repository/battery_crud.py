from sqlalchemy.orm import Session
from database.battery import Battery
from schemas.battery_scheme import BatteryCreate


def get_battery(db: Session, battery_id: int):
    return db.query(Battery).filter(Battery.id == battery_id).first()


def get_battery_by_serial(db: Session, serial_number: str):
    return db.query(Battery).filter(Battery.serial_number == serial_number).first()


def get_batteries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Battery).offset(skip).limit(limit).all()


def create_battery(db: Session, battery: BatteryCreate):
    db_battery = Battery(
        serial_number=battery.serial_number,
        capacity=battery.capacity,
        comments=battery.comments
    )
    db.add(db_battery)
    db.commit()
    db.refresh(db_battery)
    return db_battery


def update_battery(db: Session, battery_id: int, battery: BatteryCreate):
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if db_battery:
        db_battery.serial_number = battery.serial_number
        db_battery.capacity = battery.capacity
        db_battery.comments = battery.comments
        db.commit()
        db.refresh(db_battery)
    return db_battery


def delete_battery(db: Session, battery_id: int):
    db_battery = db.query(Battery).filter(Battery.id == battery_id).first()
    if db_battery:
        db.delete(db_battery)
        db.commit()
    return db_battery
