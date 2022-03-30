from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import blog

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def get_all_blog(db: Session = Depends(get_db)):
    return blog.get_all_blog(db)


@router.get("/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    return blog.get_blog_by_id(blog_id,db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(request, db)


@router.delete("/{blog_id}")
def delete_blog(blog_id, db: Session = Depends(get_db)):
    return blog.delete_blog(blog_id, db)


@router.put("/{blog_id}")
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(blog_id, request, db)
