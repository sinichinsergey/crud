from sqlalchemy.orm import Session

from models import Email


def get_emails(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Email).offset(skip).limit(limit).all()


def get_email_by_email_id(db: Session, email_id: int):
    return db.query(Email).filter(Email.email_id == email_id).first()


def get_email_by_user_id(db: Session, user_id: int):
    return db.query(Email).filter(Email.user_id == user_id).first()


def create_email(db: Session, email: Email):
    _email = Email(
        user_id=email.user_id,
        email_type=email.email_type,
        email_addr=email.email_addr)
    db.add(_email)
    db.commit()
    db.refresh(_email)
    return _email


def remove_email_by_email_id(db: Session, email_id: int):
    _email = get_email_by_email_id(db=db, email_id=email_id)
    db.delete(_email)
    db.commit()


def remove_email_by_user_id(db: Session, user_id: int):
    _email = get_email_by_user_id(db=db, user_id=user_id)
    db.delete(_email)
    db.commit()


def update_email(db: Session, email_id: int, email: Email):
    _email = get_email_by_email_id(db=db, email_id=email_id)
    _email.user_id = email.user_id
    _email.email_type = email.email_type
    _email.email_addr = email.email_addr
    db.commit()
    db.refresh(_email)
    return _email
