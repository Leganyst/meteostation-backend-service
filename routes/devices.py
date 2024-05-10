from http.server import BaseHTTPRequestHandler
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from fastapi import routing, HTTPException, Depends, status, Response

from database.db import engine
from routes.models import DataDevice, DeviceAPI
# from utils.pars_data import parse_multiple_data
from utils.parse import parse_datetime
from utils.tokens import get_current_user
from database.models.models import Device, Snapshot, RainfallSnapshot, WindSnapshot, AirSnapshot, \
    SoilSnapshot, DeviceSnapshot, ErrorSnapshot

import datetime

device_api = routing.APIRouter()

@device_api.post("/api/devices", tags=["Устройства"], response_model=DeviceAPI,
                 responses={
                     status.HTTP_409_CONFLICT: {
                         "description": "Device already exists",
                                "content": {
                                    "application/json": {
                                        "example": {"detail": "Device already exists"}
                                        }
                                    }
                                }
                     ,})
def add_device(device: DeviceAPI, response: Response, user: dict = Depends(get_current_user), ):
    exception = user.get('exception')
    if exception:
        raise exception

    with Session(engine) as session:
        new_device = Device(
            name=device.name,
            id=device.id,
        )
        session.add(new_device)
        result_device = DeviceAPI(
            name=device.name,
            id=device.id
        )
        try:
            session.commit()
        except:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Device already exists")
        response.status_code = status.HTTP_201_CREATED
        return result_device


@device_api.get("/api/devices/{id}", tags=["Устройства"], response_model=DeviceAPI,
                responses={
                    status.HTTP_404_NOT_FOUND: {
                        "description": "Device not found",
                        "content": {
                            "application/json": {
                                "example": {"detail": "Device not found"}
                            }
                        }
                    }
                })
def check_device(id: str, response: Response, user: dict = Depends(get_current_user)):
    exception = user.get('exception')
    if exception:
        raise exception
    with Session(engine) as session: 
        device = session.scalar(select(Device).where(Device.id == id))
        if device:
            response.status_code = status.HTTP_200_OK
            result_device = DeviceAPI(
                name=device.name,
                id=device.id
            )
            return result_device
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

@device_api.post("/api/devices/{id}/data", tags=["Устройства"], responses={
    status.HTTP_201_CREATED: {
        "description": "Data received successfully",
        "content": {
            "application/json": {
                "example": {"detail": "Data received successfully"}
            }
        }
    }
})
def receive_data_from_device(data: DataDevice, id: str, response: Response):
    with Session(engine) as session:
        device = session.scalar(select(Device).where(Device.id == id))
        if not device:
            device = Device(id=id, name=data.device_name if data.device_name else None)
            session.add(device)
            session.flush()
            
        rainfall = RainfallSnapshot(
            rainfall_dt=parse_datetime(data.rainfall_dt),
            rainfall=data.rainfall,
        )
        wind = WindSnapshot(
            wind_direction_dt=parse_datetime(data.wind_direction_dt),
            wind_direction=data.wind_direction,
            wind_speed_dt=parse_datetime(data.wind_speed_dt),
            wind_speed=data.wind_speed,
        )
        
        air = AirSnapshot(
            air_temperature_dt=parse_datetime(data.air_temperature_dt),
            air_temperature=data.air_temperature,
            air_pressure_dt=parse_datetime(data.air_pressure_dt),
            air_pressure=data.air_pressure,
            air_humidity_dt=parse_datetime(data.air_humidity_dt),
            air_humidity=data.air_humidity,
        )
        

        soil = SoilSnapshot(
            soil_temperature_dt=parse_datetime(data.soil_temperature_dt),
            soil_temperature=data.soil_temperature,
            soil_humidity_dt=parse_datetime(data.soil_humidity_dt),
            soil_humidity=data.soil_humidity,
        )
        
        
        device_snapshot = DeviceSnapshot(
            battery_voltage_dt=parse_datetime(data.battery_voltage_dt),
            battery_voltage=data.battery_voltage,
            gps_latitude=data.gps_latitude,
            gps_longitude=data.gps_longitude,
        )
        
        error = ErrorSnapshot(
            wind_direction_error=data.wind_direction_error,
            wind_speed_error=data.wind_speed_error,
            rainfall_error=data.rainfall_error,
            air_temperature_error=data.air_temperature_error,
            air_pressure_error=data.air_pressure_error,
            air_humidity_error=data.air_humidity_error,
            soil_temperature_error=data.soil_temperature_error,
            soil_humidity_error=data.soil_humidity_error,
            flash_card_error=data.flash_card_error,
            battery_error=data.battery_error,
            gps_error=data.gps_error,
            crash_error=data.crash_error,
        )
        snapshots = [device, rainfall, wind, air, soil, device_snapshot, error]
        for snapshot in snapshots:
            session.add(snapshot)
        session.flush()
        
        snapshot_add = Snapshot(
            device_id=device.id,
            rainfall_snapshot_id=rainfall.id,
            wind_snapshot_id=wind.id,
            air_snapshot_id=air.id,
            soil_snapshot_id=soil.id,
            device_state_snapshot_id=device_snapshot.id,
            error_snapshot_id=error.id
        )
        session.add(snapshot_add)
        session.commit()