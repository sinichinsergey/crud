from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from crud import phone as crud_phone
from schemas import Phone
from database import SessionLocal

router = APIRouter()

PHONE_TYPE_DESCRIPTION = "phone_type: False == Городской, True == Мобильный"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
        "/{user_id}/phone",
        response_model=Phone,
        description=PHONE_TYPE_DESCRIPTION)
def read_phone_by_user_id(user_id: int, db: Session = Depends(get_db)):
    _phone = crud_phone.get_phone_by_user_id(db, user_id=user_id)
    if _phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    return _phone


@router.delete("/{user_id}/phone/delete")
def delete_phone_by_user_id(user_id: int, db: Session = Depends(get_db)):
    _phone = crud_phone.get_phone_by_user_id(db, user_id=user_id)
    if _phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    crud_phone.remove_phone_by_user_id(db, user_id=user_id)
    return f"Success delete phone by user_id = {user_id}"
