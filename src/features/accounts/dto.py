from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(max_length=20, min_length=1)
    last_name: str = Field(max_length=20, min_length=1)
    email: EmailStr = Field(max_length=255)
    

class UserCreateDTO(UserBase):
    hashed_password: str
