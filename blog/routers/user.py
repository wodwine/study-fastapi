from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models
from ..hashing import Hash

router = APIRouter()

get_db = database.get_db


@router.post("/user", response_model=schemas.ShowUserWithBlog, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    request = request.dict()
    request["password"] = hashed_password
    new_user = models.User(**request)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user", response_model=List[schemas.ShowUserWithBlog], tags=["users"])
def get_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/user/{user_id}", response_model=schemas.ShowUserWithBlog, tags=["users"])
def get_user_by_id(user_id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id: {user_id} is not found")
    return user
