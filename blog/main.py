import uvicorn
from fastapi import FastAPI, Depends, Response, HTTPException, status
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return "Blog API"


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{blog_id}")
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        blog.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"Blog id: {blog_id} is deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with the id: {blog_id} is not found")


@app.put("/blog/{blog_id}")
def update_blog(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if blog.first():
        blog.update(request.dict())
        db.commit()
        return {"detail": f"Blog id: {blog_id} is updated"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Blog with the id: {blog_id} is not found")


@app.get('/blog',response_model=List[schemas.ShowBlog])
def get_all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=200,response_model=schemas.ShowBlog)
def get_blog_by_id(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id: {blog_id} is not found")
    return blog


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # uvicorn blog.main:app --reload
