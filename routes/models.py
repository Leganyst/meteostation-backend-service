from pydantic import BaseModel

class UserAPI(BaseModel):
    display_name: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    tokens_type: str
    