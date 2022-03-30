from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def get_all_blog(db: Session):
    return db.query(models.Blog).all()


def get_blog_by_id(blog_id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id: {blog_id} is not found")
    return blog


def create_blog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(**request.dict(), user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(blog_id, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        blog.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"Blog id: {blog_id} is deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with the id: {blog_id} is not found")


def update_blog(blog_id, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        blog.update(request.dict())
        db.commit()
        return {"detail": f"Blog id: {blog_id} is updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with the id: {blog_id} is not found")
