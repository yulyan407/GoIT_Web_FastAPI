from datetime import date
from pydantic import BaseModel, EmailStr, Field, PastDate, ConfigDict
from pydantic_extra_types.phone_numbers import PhoneNumber
from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    surname: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(min_length=7, max_length=50)
    phone: PhoneNumber
    birthday: date = Field(PastDate())


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: str
    phone: str
    birthday: date
    user: UserResponse | None

    model_config = ConfigDict(from_attributes=True)  # noqa