from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from fastapi import Response, routing, Depends, HTTPException, status

from database.db import engine
from database.models.models import Device, UserDevice, User
from utils.tokens import get_current_user
from routes.models import DeviceAPI, UserAPI, UserDevices

from uuid import UUID

user_api = routing.APIRouter()

@user_api.get("/api/users", tags=["Пользователи"], response_model=UserDevices)
def get_devices_user(user: dict = Depends(get_current_user)):
    exception = user.get('exception')
    if exception:
        raise exception
    else:
        with Session(engine) as session:
            query = select(User).where(User.email==user.get('sub')).options(joinedload(User.devices))
            user = session.scalars(query).first()
            
            if user:
                devices = [device.id for device in user.devices]
                return (UserDevice(user=user.email, devices=devices))
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User devices not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
                
@user_api.post("/api/user/device", tags=["Пользователи"],
               response_model=DeviceAPI, responses={
                   status.HTTP_404_NOT_FOUND: {
                       "description": "User or device not found",
                       "content": {
                           "application/json": {
                               "example": {"detail": "User not found"}
                           }
                       }
                   },
                   status.HTTP_400_BAD_REQUEST: {
                       "description": "This Devise already added to this user",
                       "content": {
                           "application/json": {
                               "example": {"Device already added to this user"}
                           }
                       }
                   }
               })
def add_device_user(device: DeviceAPI, response: Response, user: dict = Depends(get_current_user)):
    with Session(engine) as session:
        exception = user.get('exception')
        if exception:
            raise exception
        user = session.query(User).filter(User.email == user.get('sub')).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        device_exists = session.query(Device).filter(Device.id == device.id).first()
        if not device_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        user_device = session.query(UserDevice).filter_by(user_id=user.id, device_id=device_exists.id).first()
        if user_device:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device already added to this user")
        
        new_user_device = UserDevice(user_id=user.id, device_id=device_exists.id) 
        session.add(new_user_device)
        session.commit()
        response.status_code = status.HTTP_201_CREATED
        return device
    
@user_api.delete("/api/user/device", tags=["Пользователи"],
                 responses={
                     status.HTTP_404_NOT_FOUND: {
                         "description": "User or device not found",
                         "content": {
                             "application/json": {
                                 "example": {"detail": "User not found"}
                             }
                         }
                     },
                     status.HTTP_204_NO_CONTENT: {
                         "description": "Device deleted from user",
                         "content": {
                             "application/json": {
                                 "example": {"detail": "Device deleted from user"}
                             }
                         }
                     }
                 })
def delete_device_user(device: DeviceAPI, response: Response, user: dict = Depends(get_current_user)):
    with Session(engine) as session:
        exception = user.get('exception')
        if exception:
            raise exception
        user = session.query(User).filter(User.email == user.get('sub')).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        device_exists = session.query(Device).filter(Device.id == device.id).first()
        if not device_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")

        user_device = session.query(UserDevice).filter_by(user_id=user.id, device_id=device_exists.id).first()
        if user_device:
            session.delete(user_device)
            session.commit()
            response.status_code = status.HTTP_204_NO_CONTENT
            return JSONResponse(content={"detail": "Device deleted from user"})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")


@user_api.delete("/api/user", tags=["Пользователи"], responses={
    status.HTTP_404_NOT_FOUND: {
        "description": "User or device not found",
        "content": {
            "application/json": {
                "example": {"detail": "User not found"}
            }
        }
    },
    status.HTTP_204_NO_CONTENT: {
        "description": "User profile deleted",
        "content": {
            "application/json": {
                "example": {"204": "User profile deleted"}
            }
        }
    }
})
def delete_profile_user(response: Response, user: dict = Depends(get_current_user)):
    with Session(engine) as session:
        exception = user.get('exception')
        if exception:
            raise exception
        user = session.query(User).filter(User.email == user.get('sub')).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        session.delete(user)
        session.commit()
        response.status_code = status.HTTP_204_NO_CONTENT
        return JSONResponse({204: "User profile deleted"})