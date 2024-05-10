from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserAPI(BaseModel):
    """
    Представляет собой модель юзера в API. Содержит в себе три обязательых поля

    Атрибуты:
    display_name - ФИО пользователя
    
    email - электронная почта пользователя
    
    password - пароль
    """
    display_name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    tokens_type: str

class UserDevices(BaseModel):
    user: str
    devices: list | None
    
class DeviceAPI(BaseModel):
    name: Optional[str] = None
    id: str

class DataDevice(BaseModel):
    device_name: Optional[str] = None
    
    wind_direction_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    wind_direction: Optional[int] = None
    
    wind_speed_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    wind_speed: Optional[int] = None
    
    rainfall_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    rainfall: Optional[int] = None
    
    air_temperature_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    air_temperature: Optional[int] = None
    
    air_pressure_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    air_pressure: Optional[int] = None
    
    air_humidity_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    air_humidity: Optional[int] = None
    
    soil_temperature_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    soil_temperature: Optional[int] = None
    
    soil_humidity_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    soil_humidity: Optional[int] = None
    
    battery_voltage_dt: Optional[str] = Field(
        default=None,
        description='Datetime string: "09.05.2024, 17:41:30" ')
    battery_voltage: Optional[int] = None
    
    gps_latitude: Optional[int] = None
    gps_longitude: Optional[int] = None
    
    wind_direction_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    wind_speed_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    rainfall_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    air_temperature_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    air_pressure_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    air_humidity_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    soil_temperature_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    soil_humidity_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    flash_card_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    battery_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    gps_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    crash_error: Optional[str] = Field(
        default=None,
        description='datetime string and errors text:' 
        '"09.05.2024, 17:41:30, text"')
    
    