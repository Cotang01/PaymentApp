from typing import ClassVar, Self, TypeVar

from pydantic import BaseModel, EmailStr, Field, model_validator

from src.features.accounts.dto import UserBase

T = TypeVar("T")


class UserCreate(UserBase):
    """schema for creating user, has required data to save user to db"""
    password: str = Field(max_length=255, min_length=8)


class UserUpdate(UserBase):
    """schema for updating user, all fields are required to save them to db"""
    password: str = Field(max_length=255, min_length=8)


class UserPatch(BaseModel):
    """schema for updating user, has optional data to save to db"""
    first_name: str | None = Field(default=None, max_length=20)
    last_name: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def check_if_any_field_set(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("At least one field must be set")
        return self
    
    
class UserResponse(UserBase):
    """schema for output user, lacks sensitive data"""
    id: int
    
    model_config: ClassVar = {"from_attributes": True}


class PageResponse[T](BaseModel):
    items: list[T]
    limit: int
    offset: int


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # clear contract with Oauth2
   
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
