from datetime import date
import re

from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    user_name: str = Field(
        default="Фамилия Имя Отчество",
        regex='^[А-ЯЁа-яё]{1,15}\s[А-ЯЁа-яё]{1,15}\s[А-ЯЁа-яё]{1,15}$')
    user_gender: bool = Field(description="False == М, True == Ж")
    user_birthdate: date = None
    user_addr: str = Field(default="г. Красноярск", max_length=100)


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class PhoneBase(BaseModel):
    user_id: int = Field(..., gt=0)
    phone_type: bool = Field(
        description="False == Городской, True == Мобильный")
    phone_num: str = Field(default="00000000000", regex="^[0-9]{11}$")


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    phone_id: int = Field(..., gt=0)

    class Config:
        orm_mode = True


class EmailBase(BaseModel):
    user_id: int = Field(..., gt=0)
    email_type: bool = Field(description="False == Личная, True == Рабочая")
    email_addr: str = Field(default="net@mail.ru", max_length=100)

    @validator('email_addr')
    def check(cls, v: str) -> str:
        regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        if not (re.fullmatch(regex, v)):
            raise ValueError("Invalid email. Should be like example@mail.com")
        return v


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    email_id: int = Field(..., gt=0)

    class Config:
        orm_mode = True
