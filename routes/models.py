from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field

class UserAPI(BaseModel):
    """
    Представляет собой модель пользователя в API, содержащую основные учетные данные пользователя.
    """
    display_name: str = Field(..., description="ФИО пользователя, используемое для идентификации на платформе.", example="Иван Иванов")
    email: str = Field(..., description="Электронная почта пользователя, используемая как логин для доступа к системе.", example="ivan.ivanov@example.com")
    password: str = Field(..., description="Пароль для входа в систему. Должен быть надежным и содержать комбинацию букв и цифр.", example="SecurePassword123!")


from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    """
    Представляет собой модель токена, содержит всегда access токен и возможно refresh, а так же тип токенов
    """
    access_token: str = Field(..., description="Токен доступа, используемый для аутентификации запросов.",
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    refresh_token: Optional[str] = Field(None, description="Необязательный токен обновления, используемый для получения нового токена доступа после его истечения.",
                                         example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    tokens_type: str = Field(..., description="Тип токена, обычно используется для указания метода аутентификации.", example="Bearer")



class UserDevices(BaseModel):
    """
    Представляет собой модель данных, которая содержит информацию о пользователе и его устройствах.
    """
    user: str = Field(..., description="Идентификатор пользователя или его электронная почта.", example="ivan.ivanov@example.com")
    devices: Optional[List[str]] = Field(None, description="Список идентификаторов устройств, связанных с пользователем.", example=["device1", "device2", "device3"])
    
    
class DeviceAPI(BaseModel):
    """
    Представляет собой модель данных для устройства, содержащую его идентификатор и опциональное имя.
    """
    name: Optional[str] = Field(None, description="Имя устройства. Может быть не указано.", example="Датчик воздуха")
    id: str = Field(..., description="Уникальный идентификатор устройства в системе.", example="device123")

from pydantic import BaseModel, Field
from typing import Optional

class DataDevice(BaseModel):
    """
    Модель данных, собираемых с устройства, включая метеорологические данные и состояние оборудования.
    """
    device_name: Optional[str] = Field(None, description="Название устройства", example="Метеостанция Alpha")
    # Данные и метки времени для каждого параметра
    wind_direction_dt: Optional[str] = Field(None, description="Дата и время измерения направления ветра", example="09.05.2024, 17:41:30")
    wind_direction: Optional[int] = Field(None, description="Измеренное направление ветра в градусах", example=180)
    wind_speed_dt: Optional[str] = Field(None, description="Дата и время измерения скорости ветра", example="09.05.2024, 17:41:30")
    wind_speed: Optional[int] = Field(None, description="Измеренная скорость ветра в м/с", example=5)
    rainfall_dt: Optional[str] = Field(None, description="Дата и время измерения количества осадков", example="09.05.2024, 17:41:30")
    rainfall: Optional[int] = Field(None, description="Измеренное количество осадков в мм", example=2)
    air_temperature_dt: Optional[str] = Field(None, description="Дата и время измерения температуры воздуха", example="09.05.2024, 17:41:30")
    air_temperature: Optional[int] = Field(None, description="Измеренная температура воздуха в градусах Цельсия", example=22)
    air_pressure_dt: Optional[str] = Field(None, description="Дата и время измерения давления воздуха", example="09.05.2024, 17:41:30")
    air_pressure: Optional[int] = Field(None, description="Измеренное давление воздуха в гПа", example=1013)
    air_humidity_dt: Optional[str] = Field(None, description="Дата и время измерения влажности воздуха", example="09.05.2024, 17:41:30")
    air_humidity: Optional[int] = Field(None, description="Измеренная влажность воздуха в процентах", example=75)
    soil_temperature_dt: Optional[str] = Field(None, description="Дата и время измерения температуры почвы", example="09.05.2024, 17:41:30")
    soil_temperature: Optional[int] = Field(None, description="Измеренная температура почвы в градусах Цельсия", example=18)
    soil_humidity_dt: Optional[str] = Field(None, description="Дата и время измерения влажности почвы", example="09.05.2024, 17:41:30")
    soil_humidity: Optional[int] = Field(None, description="Измеренная влажность почвы в процентах", example=30)
    battery_voltage_dt: Optional[str] = Field(None, description="Дата и время последней проверки напряжения батареи", example="09.05.2024, 17:41:30")
    battery_voltage: Optional[int] = Field(None, description="Напряжение батареи в вольтах", example=12)
    gps_latitude: Optional[int] = Field(None, description="Широта местоположения устройства", example=55)
    gps_longitude: Optional[int] = Field(None, description="Долгота местоположения устройства", example=37)
    # Поля для описания возможных ошибок в данных
    wind_direction_error: Optional[str] = Field(None, description="Описание ошибки в данных направления ветра")
    wind_speed_error: Optional[str] = Field(None, description="Описание ошибки в данных скорости ветра")
    rainfall_error: Optional[str] = Field(None, description="Описание ошибки в данных осадков")
    air_temperature_error: Optional[str] = Field(None, description="Описание ошибки в данных температуры воздуха")
    air_pressure_error: Optional[str] = Field(None, description="Описание ошибки в данных давления воздуха")
    air_humidity_error: Optional[str] = Field(None, description="Описание ошибки в данных влажности воздуха")
    soil_temperature_error: Optional[str] = Field(None, description="Описание ошибки в данных температуры почвы")
    soil_humidity_error: Optional[str] = Field(None, description="Описание ошибки в данных влажности почвы")
    flash_card_error: Optional[str] = Field(None, description="Описание ошибки чтения данных с флеш-карты")
    battery_error: Optional[str] = Field(None, description="Описание ошибки состояния батареи")
    gps_error: Optional[str] = Field(None, description="Описание ошибки в данных GPS")
    crash_error: Optional[str] = Field(None, description="Описание ошибки краха системы")
