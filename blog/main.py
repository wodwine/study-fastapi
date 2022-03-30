import uvicorn
from fastapi import FastAPI
from . import schemas

app = FastAPI()


@app.get("/")
def index():
    return "Blog API"


@app.post("/blog")
def create(request: schemas.Blog):
    return request


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # uvicorn blog.main:app --reload
