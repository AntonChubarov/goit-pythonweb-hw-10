from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    email_confirmed: bool

    class Config:
        orm_mode = True
        from_attributes = True


class UserUpdate(BaseModel):
    username: str
    email: EmailStr

class UserInDB(UserCreate):
    hashed_password: str
