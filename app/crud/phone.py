from sqlalchemy.orm import Session

from models import Phone


def get_phones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Phone).offset(skip).limit(limit).all()


def get_phone_by_phone_id(db: Session, phone_id: int):
    return db.query(Phone).filter(Phone.phone_id == phone_id).first()


def get_phone_by_user_id(db: Session, user_id: int):
    return db.query(Phone).filter(Phone.user_id == user_id).first()


def create_phone(db: Session, phone: Phone):
    _phone = Phone(
        user_id=phone.user_id,
        phone_type=phone.phone_type,
        phone_num=phone.phone_num)
    db.add(_phone)
    db.commit()
    db.refresh(_phone)
    return _phone


def remove_phone_by_phone_id(db: Session, phone_id: int):
    _phone = get_phone_by_phone_id(db=db, phone_id=phone_id)
    db.delete(_phone)
    db.commit()


def remove_phone_by_user_id(db: Session, user_id: int):
    _phone = get_phone_by_user_id(db=db, user_id=user_id)
    db.delete(_phone)
    db.commit()


def update_phone(db: Session, phone_id: int, phone: Phone):
    _phone = get_phone_by_phone_id(db=db, phone_id=phone_id)
    _phone.user_id = phone.user_id
    _phone.phone_type = phone.phone_type
    _phone.phone_num = phone.phone_num
    db.commit()
    db.refresh(_phone)
    return _phone
