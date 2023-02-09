from sqlalchemy import Boolean, Column, Integer, String, Date

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_gender = Column(Boolean)  # False = М, True = Ж
    user_birthdate = Column(Date)
    user_addr = Column(String)


class Phone(Base):
    __tablename__ = "phones"

    phone_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    phone_type = Column(Boolean)  # False = Городской, True = Мобильный
    phone_num = Column(String)


class Email(Base):
    __tablename__ = "emails"

    email_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    email_type = Column(Boolean)  # False = Личная, True = Рабочая
    email_addr = Column(String)
