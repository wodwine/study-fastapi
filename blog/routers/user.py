from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2
from ..repository import user

router = APIRouter(prefix="/user", tags=["Users"])

get_db = database.get_db


@router.post("/", response_model=schemas.ShowUserWithBlog)
def create_user(request: schemas.User, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.create_user(request, db)


@router.get("/", response_model=List[schemas.ShowUserWithBlog])
def get_all_user(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_all_user(db)


@router.get("/{user_id}", response_model=schemas.ShowUserWithBlog)
def get_user_by_id(user_id, db: Session = Depends(get_db),
                   current_user: schemas.User = Depends(oauth2.get_current_user)):
    return user.get_user_by_id(user_id, db)
