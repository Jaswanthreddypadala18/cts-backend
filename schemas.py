
from pydantic import BaseModel, EmailStr

class SignupSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class SigninSchema(BaseModel):
    email: EmailStr
    password: str

class CreateGroupSchema(BaseModel):
    group_name: str

class AvailabilitySchema(BaseModel):
    from_time: str
    to_time: str






