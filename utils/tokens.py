from datetime import datetime, timedelta, UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict, expires_delta: timedelta = None) -> str:
    # В словаре передается в data только те данные, которые надо хранить в токене
    # В данном случае это почта пользователя для его валидации
    # expire - срок истечения токена. Его мы тоже передадим при вызове, и это объект timedelta
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        # Если не передан, тогда по умолчанию срок истечения 15 минут
        expire = datetime.now(UTC) + timedelta(minutes=15)
    # Добавляем в словарь срок годности токена
    to_encode.update({"exp": expire})
    # И энкодим в JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token: str) -> dict | None:
    try:
        # Получаем словарь обратно
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # в sub (в функции при вызове) мы передаём почту юзера 
        email: str = payload.get('sub')
        if email is None:
            # Если её нет
            raise JWTError("Token payload missing required failed")
        
        expiration = payload.get('exp')
        if expiration is None:
            # Если нет срока годности
            raise JWTError("Token payload missing expiration")
        
        # Вычисляем теперь срок истечения токена
        expire = datetime.fromtimestamp(expiration, tz=UTC)
        if datetime.now(UTC) > expire:
            raise JWTError("Token expired")
        # В конце концов, возвращаем раскодированный словарь из токена
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Получаем словарь из токена
    payload = validate_token(token)
    # Если словаря есть и есть ключ sub, тогда мы возвращаем просто почту пользователя
    if payload is not None and "sub" in payload:
        payload.update({"result": True})
        return payload
    else:
        return {
            "result": False,
            "exception": credentials_exception
            }
        
    