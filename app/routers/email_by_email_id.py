from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from crud import email as crud_email
from schemas import Email, EmailBase
from database import SessionLocal
from logger import logger

router = APIRouter()

EMAIL_TYPE_DESCRIPTION = "email_type: False == Личная, True == Рабочая"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
        "/",
        response_model=list[Email],
        description=EMAIL_TYPE_DESCRIPTION)
def read_all_emails(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _emails = crud_email.get_emails(db, skip=skip, limit=limit)
    return _emails


@router.post(
        "/{email_id}",
        response_model=Email,
        description=EMAIL_TYPE_DESCRIPTION)
def read_email_by_email_id(email_id: int, db: Session = Depends(get_db)):
    _email = crud_email.get_email_by_email_id(db, email_id=email_id)
    if _email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return _email


@router.put(
        "/create",
        response_model=Email,
        description=EMAIL_TYPE_DESCRIPTION)
def create_email(email: EmailBase, db: Session = Depends(get_db)):
    try:
        _email = crud_email.create_email(db, email=email)
        logger.info(f'''SUCCESS create new Email:
            user_id = {email.user_id},
            email_type = {email.email_type},
            email_addr = {email.email_addr}'''.replace("            ", ""))
        return _email
    except Exception as _ex:
        logger.info(f'ERROR   while creating Email: {_ex}', _ex)


@router.delete("/{email_id}/delete")
def delete_email_by_email_id(email_id: int, db: Session = Depends(get_db)):
    _email = crud_email.get_email_by_email_id(db, email_id=email_id)
    if _email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    crud_email.remove_email_by_email_id(db, email_id=email_id)
    return f"Success delete email by email_id = {email_id}"


@router.patch(
        "/{email_id}/update",
        response_model=Email,
        description=EMAIL_TYPE_DESCRIPTION)
def update_email(
        email_id: int, email: EmailBase,
        db: Session = Depends(get_db)):
    _email = crud_email.get_email_by_email_id(db, email_id=email_id)
    if _email is None:
        logger.info('ERROR   while updating Email: 404 Email not found')
        raise HTTPException(status_code=404, detail="Email not found")
    try:
        _email = crud_email.update_email(db, email_id=email_id, email=email)
        logger.info(f'''SUCCESS updating Email:
            email_id = {email_id},
            user_id = {email.user_id},
            email_type = {email.email_type},
            email_addr = {email.email_addr}'''.replace("            ", ""))
        return _email
    except Exception as _ex:
        logger.info(f'ERROR   while updating Email: {_ex}', _ex)
