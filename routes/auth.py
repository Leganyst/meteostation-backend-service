from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import routing
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database.db import engine
from config import app, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from database.models.models import User
from routes.models import UserAPI, Token
from utils.hash import validate_password_hash, generate_password_hash
from utils.tokens import create_token, get_current_user, validate_token

from datetime import timedelta

auth = routing.APIRouter()

@auth.post("/register", response_model=Token, tags=["Авторизация"])
def register(user: UserAPI):
    with Session(engine) as session:
        result = session.execute(select(User).where(User.email == user.email)).one_or_none()
        if result is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        hashed_password = generate_password_hash(user.password)

        new_user = User(
            email=user.email,
            password=hashed_password,
            display_name=user.display_name,
            role="user"
        )
        session.add(new_user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        access_token = create_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        refresh_token = create_token(
            data={"sub": user.email}, expires_delta=refresh_token_expires
        )
        token = Token(access_token=access_token, tokens_type="bearer", refresh_token=refresh_token)
        session.commit()
        return token

@auth.post("/token", response_model=Token, tags=["Авторизация"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Поле username технически остается username, но фактически его можно использовать 
    # и для почты
    user = validate_password_hash(form_data.password, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": form_data.username}, expires_delta=refresh_token_expires
    )
    token = Token(access_token=access_token, tokens_type="bearer", refresh_token=refresh_token)
    return token

@auth.post("/refresh", response_model=Token, tags=["Авторизация"])
def new_access_token(current_user: dict = Depends(get_current_user)):
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": current_user.get('sub')}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, tokens_type="bearer")

@auth.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    if "exception" not in current_user:
        return {"user": current_user}
    else:
        raise current_user['exception']  

