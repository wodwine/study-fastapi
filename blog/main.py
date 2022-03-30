import uvicorn
from fastapi import FastAPI
from . import schemas, models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return "Blog API"


@app.post("/blog")
def create(request: schemas.Blog):
    return request


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)  # uvicorn blog.main:app --reload
