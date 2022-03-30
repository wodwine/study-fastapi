from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database, models

router = APIRouter(prefix="/blog", tags=["Blogs"])

get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(**request.dict(), user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/{blog_id}")
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        blog.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"Blog id: {blog_id} is deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with the id: {blog_id} is not found")


@router.put("/{blog_id}")
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        blog.update(request.dict())
        db.commit()
        return {"detail": f"Blog id: {blog_id} is updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with the id: {blog_id} is not found")


@router.get("/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id: {blog_id} is not found")
    return blog
