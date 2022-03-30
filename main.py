from typing import Optional

from fastapi import FastAPI
from blog import Blog

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/about")
def about():
    return {"data": "This API is used for learn about FastAPI"}


@app.get("/blog")
def blog(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published data is processing"}
    return {"data": f"{limit} unpublished data is processing"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "This is a secret"}


@app.get("/blog/{blog_id}")
def blog(blog_id: int):
    return {"Blog": blog_id}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id: int):
    return {"Blog": blog_id, "comment": "Hello World"}


@app.post("/blog")
def create_blog(request: Blog):
    return {"data": f"Blog is created with title as: \"{request.title}\""}
