from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash


def get_all_user(db: Session):
    return db.query(models.User).all()


def get_user_by_id(user_id, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id: {user_id} is not found")
    return user


def create_user(request: schemas.User, db: Session):
    hashed_password = Hash.bcrypt(request.password)
    request = request.dict()
    request["password"] = hashed_password
    new_user = models.User(**request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
