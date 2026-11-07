from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: EmailStr
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.second_name}"


class UserCreate(UserBase):
    """schema for creating user, has required data to save user to db"""
    # password: str

    model_config = {"from_attributes": True}


class UserUpdate(UserBase):
    """schema for updating user, has optional data to save user to db"""
    # password: str


class UserResponse(UserBase):
    id: int
    
    model_config = {"from_attributes": True}