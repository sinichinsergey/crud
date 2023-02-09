from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from crud import email as crud_email
from schemas import Email
from database import SessionLocal

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
        "/{user_id}/email",
        response_model=Email,
        description=EMAIL_TYPE_DESCRIPTION)
def read_email_by_user_id(user_id: int, db: Session = Depends(get_db)):
    _email = crud_email.get_email_by_user_id(db, user_id=user_id)
    if _email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    return _email


@router.delete("/{user_id}/email/delete")
def delete_email_by_user_id(user_id: int, db: Session = Depends(get_db)):
    _email = crud_email.get_email_by_user_id(db, user_id=user_id)
    if _email is None:
        raise HTTPException(status_code=404, detail="Email not found")
    crud_email.remove_email_by_user_id(db, user_id=user_id)
    return f"Success delete email by user_id = {user_id}"
