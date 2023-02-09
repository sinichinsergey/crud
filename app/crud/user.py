from sqlalchemy.orm import Session

from models import User


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db: Session, user: User):
    _user = User(
        user_name=user.user_name,
        user_gender=user.user_gender,
        user_birthdate=user.user_birthdate,
        user_addr=user.user_addr.strip())
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def remove_user(db: Session, user_id: int):
    _user = get_user_by_user_id(db=db, user_id=user_id)
    db.delete(_user)
    db.commit()


def update_user(db: Session, user_id: int, user: User):
    _user = get_user_by_user_id(db=db, user_id=user_id)
    _user.user_name = user.user_name
    _user.user_gender = user.user_gender
    _user.user_birthdate = user.user_birthdate
    _user.user_addr = user.user_addr.strip()
    db.commit()
    db.refresh(_user)
    return _user
