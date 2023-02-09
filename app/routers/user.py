from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from crud import user as crud_user
from schemas import User, UserBase
from database import SessionLocal
from logger import logger

router = APIRouter()

USER_GENDER_DESCRIPTION = "user_gender: False == М, True == Ж"


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
        "/",
        response_model=list[User],
        description=USER_GENDER_DESCRIPTION)
def read_all_users(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _users = crud_user.get_users(db, skip=skip, limit=limit)
    return _users


@router.post(
        "/{user_id}",
        response_model=User,
        description=USER_GENDER_DESCRIPTION)
def read_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    _user = crud_user.get_user_by_user_id(db, user_id=user_id)
    if _user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _user


@router.put(
        "/create",
        response_model=User,
        description=USER_GENDER_DESCRIPTION)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    try:
        _user = crud_user.create_user(db, user=user)
        logger.info(f'''SUCCESS create new User:
            user_name = {user.user_name},
            user_gender = {user.user_gender},
            user_birthdate = {user.user_birthdate},
            user_addr = {user.user_addr}'''.replace("            ", ""))
        return _user
    except Exception as _ex:
        logger.info(f'ERROR   while creating User: {_ex}', _ex)


@router.delete("/{user_id}/delete")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    _user = crud_user.get_user_by_user_id(db, user_id=user_id)
    if _user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.remove_user(db, user_id=user_id)
    return f"Success delete user by user_id = {user_id}"


@router.patch(
        "/{user_id}/update",
        response_model=User,
        description=USER_GENDER_DESCRIPTION)
def update_user(
        user_id: int, user: UserBase, db: Session = Depends(get_db)):
    _user = crud_user.get_user_by_user_id(db, user_id=user_id)
    if _user is None:
        logger.info('ERROR   while updating User: 404 User not found')
        raise HTTPException(status_code=404, detail="User not found")
    try:
        _user = crud_user.update_user(db, user_id=user_id, user=user)
        logger.info(f'''SUCCESS updating User:
            user_id = {user_id},
            user_name = {user.user_name},
            user_gender = {user.user_gender},
            user_birthdate = {user.user_birthdate},
            user_addr = {user.user_addr}'''.replace("            ", ""))
        return _user
    except Exception as _ex:
        logger.info(f'ERROR   while updating User: {_ex}', _ex)
