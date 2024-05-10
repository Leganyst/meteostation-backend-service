from sqlalchemy import DateTime, String, ForeignKey, Column, false
from sqlalchemy.orm import Mapped,  relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from database.models.base import Base

import uuid

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # devices: Mapped[str] = mapped_column(String(255))
    
    # Во-первых нужен перечень ролей, во вторых можно хранить просто строку, а не enumerate - меньше "геморроя"
    # role: Mapped[str] = mapped_column(String(255), default="user")
    # role = mapped_column(enumerate)
    role: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    registration_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    
    devices: Mapped["Device"] = relationship("Device", secondary="user_devices", back_populates="users")

class Device(Base):
    __tablename__ = "devices"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, unique=True)
    registration_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    
    users: Mapped["User"] = relationship("User", secondary="user_devices", back_populates="devices")
    snapshots: Mapped["Snapshot"] = relationship("Snapshot", back_populates="device")

class UserDevice(Base):
    __tablename__ = "user_devices"

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False)
    device_id: Mapped[str] = mapped_column(String(255), ForeignKey("devices.id"), primary_key=True, nullable=False)

class Snapshot(Base):
    __tablename__ = "snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id: Mapped[str] = mapped_column(String(255), ForeignKey("devices.id"), primary_key=True, nullable=False)
    rainfall_snapshot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("rainfall_snapshots.id"), nullable=True)
    wind_snapshot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wind_snapshots.id"), nullable=True)
    air_snapshot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("air_snapshots.id"), nullable=True)
    soil_snapshot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("soil_snapshots.id"), nullable=True)
    device_state_snapshot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("device_snapshots.id"), nullable=True)
    error_snapshot_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("error_snapshots.id"), nullable=True)
    
    device: Mapped["Device"] = relationship("Device", back_populates="snapshots")
    rainfall_snapshot: Mapped["RainfallSnapshot"] = relationship("RainfallSnapshot", back_populates="snapshot")
    wind_snapshot: Mapped["WindSnapshot"] = relationship("WindSnapshot", back_populates="snapshot")
    air_snapshot: Mapped["AirSnapshot"] = relationship("AirSnapshot", back_populates="snapshot")
    soil_snapshot: Mapped["SoilSnapshot"] = relationship("SoilSnapshot", back_populates="snapshot")
    device_state_snapshot: Mapped["DeviceSnapshot"] = relationship("DeviceSnapshot", back_populates="snapshot")
    error_snapshot: Mapped["ErrorSnapshot"] = relationship("ErrorSnapshot", back_populates="snapshot")
    
class RainfallSnapshot(Base):
    __tablename__ = "rainfall_snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rainfall_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    rainfall: Mapped[str] = mapped_column(String(255), nullable=True)
    
    snapshot: Mapped["Snapshot"] = relationship("Snapshot", back_populates="rainfall_snapshot", uselist=False)
    
    
class WindSnapshot(Base):
    __tablename__ = "wind_snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wind_direction_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    wind_direction: Mapped[str] = mapped_column(String(255), nullable=True)
    wind_speed_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    wind_speed: Mapped[str] = mapped_column(String(255), nullable=True)
    
    snapshot: Mapped["Snapshot"] = relationship("Snapshot", back_populates="wind_snapshot", uselist=False)
    
    
class AirSnapshot(Base):
    __tablename__ = "air_snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    air_temperature_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    air_temperature: Mapped[str] = mapped_column(String(255), nullable=True)
    air_pressure_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    air_pressure: Mapped[str] = mapped_column(String(255), nullable=True)
    air_humidity_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    air_humidity: Mapped[str] = mapped_column(String(255), nullable=True)
    
    snapshot: Mapped["Snapshot"] = relationship("Snapshot", back_populates="air_snapshot", uselist=False)
    
class SoilSnapshot(Base):
    __tablename__ = "soil_snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)    
    soil_temperature_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=false)
    soil_temperature: Mapped[str] = mapped_column(String(255), nullable=True)
    soil_humidity_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    soil_humidity: Mapped[str] = mapped_column(String(255), nullable=True)

    snapshot: Mapped["Snapshot"] = relationship("Snapshot", back_populates="soil_snapshot", uselist=False)

class DeviceSnapshot(Base):
    __tablename__ = "device_snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    battery_voltage_dt: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    battery_voltage: Mapped[str] = mapped_column(String(255), nullable=True)
    gps_latitude: Mapped[str] = mapped_column(String(255), nullable=True)
    gps_longitude: Mapped[str] = mapped_column(String(255), nullable=True)
    
    snapshot: Mapped["Snapshot"] = relationship("Snapshot", back_populates="device_state_snapshot", uselist=False)
    
    
class ErrorSnapshot(Base):
    __tablename__ = "error_snapshots"
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wind_direction_error: Mapped[str] = mapped_column(String(255), nullable=True)
    wind_speed_error: Mapped[str] = mapped_column(String(255), nullable=True)
    rainfall_error: Mapped[str] = mapped_column(String(255), nullable=True)
    air_temperature_error: Mapped[str] = mapped_column(String(255), nullable=True)
    air_pressure_error: Mapped[str] = mapped_column(String(255), nullable=True)
    air_humidity_error: Mapped[str] = mapped_column(String(255), nullable=True)
    soil_temperature_error: Mapped[str] = mapped_column(String(255), nullable=True)
    soil_humidity_error: Mapped[str] = mapped_column(String(255), nullable=True)
    flash_card_error: Mapped[str] = mapped_column(String(255), nullable=True)
    battery_error: Mapped[str] = mapped_column(String(255), nullable=True)
    gps_error: Mapped[str] = mapped_column(String(255), nullable=True)
    crash_error: Mapped[str] = mapped_column(String(255), nullable=True)
    
    snapshot: Mapped["Snapshot"] = relationship("Snapshot", back_populates="error_snapshot", uselist=False)