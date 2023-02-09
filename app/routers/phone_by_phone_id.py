from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from crud import phone as crud_phone
from schemas import Phone, PhoneBase
from database import SessionLocal
from logger import logger

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
        "/",
        response_model=list[Phone],
        description=PHONE_TYPE_DESCRIPTION)
def read_all_phones(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _phones = crud_phone.get_phones(db, skip=skip, limit=limit)
    return _phones


@router.post(
        "/{phone_id}",
        response_model=Phone,
        description=PHONE_TYPE_DESCRIPTION)
def read_phone_by_phone_id(phone_id: int, db: Session = Depends(get_db)):
    _phone = crud_phone.get_phone_by_phone_id(db, phone_id=phone_id)
    if _phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    return _phone


@router.put(
        "/create",
        response_model=Phone,
        description=PHONE_TYPE_DESCRIPTION)
def create_phone(phone: PhoneBase, db: Session = Depends(get_db)):
    try:
        _phone = crud_phone.create_phone(db, phone=phone)
        logger.info(f'''SUCCESS create new Phone:
            user_id = {phone.user_id},
            phone_type = {phone.phone_type},
            phone_num = {phone.phone_num}'''.replace("            ", ""))
        return _phone
    except Exception as _ex:
        logger.info(f'ERROR   while creating Phone: {_ex}', _ex)


@router.delete("/{phone_id}/delete")
def delete_phone_by_phone_id(phone_id: int, db: Session = Depends(get_db)):
    _phone = crud_phone.get_phone_by_phone_id(db, phone_id=phone_id)
    if _phone is None:
        raise HTTPException(status_code=404, detail="Phone not found")
    crud_phone.remove_phone_by_phone_id(db, phone_id=phone_id)
    return f"Success delete phone by phone_id = {phone_id}"


@router.patch(
        "/{phone_id}/update",
        response_model=Phone,
        description=PHONE_TYPE_DESCRIPTION)
def update_phone(
        phone_id: int, phone: PhoneBase,
        db: Session = Depends(get_db)):
    _phone = crud_phone.get_phone_by_phone_id(db, phone_id=phone_id)
    if _phone is None:
        logger.info('ERROR   while updating Phone: 404 Phone not found')
        raise HTTPException(status_code=404, detail="Phone not found")
    try:
        _phone = crud_phone.update_phone(db, phone_id=phone_id, phone=phone)
        logger.info(f'''SUCCESS updating Phone:
            phone_id = {phone_id}
            user_id = {phone.user_id},
            phone_type = {phone.phone_type},
            phone_num = {phone.phone_num}'''.replace("            ", ""))
        return _phone
    except Exception as _ex:
        logger.info(f'ERROR   while updating Phone: {_ex}', _ex)
