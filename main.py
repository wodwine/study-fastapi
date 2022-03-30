from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/about")
def about():
    return {"data": "This API is used for learn about FastAPI"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "This is a secret"}


@app.get("/blog/{blog_id}")
def blog(blog_id: int):
    return {"Blog": blog_id}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id: int):
    return {"Blog": blog_id, "comment": "Hello World"}
