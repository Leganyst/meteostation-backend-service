from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import engine
from database.models.models import User

import bcrypt

def generate_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def validate_password_hash(password: str, email: str) -> bool:
    with Session(engine) as session:
        user = session.execute(select(User).where(User.email == email)).scalars().one_or_none()
        if user is None:
            return False
        password_bytes = password.encode('utf-8')
        stored_password_bytes = user.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, stored_password_bytes)
