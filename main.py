import uvicorn
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

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


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(request: Blog):
    return {"data": f"Blog is created with title as: \"{request.title}\""}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)  # uvicorn main:app --reload
