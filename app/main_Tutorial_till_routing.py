# uvicorn app.main:app --reload
# Removing all the Note Comments from the Previous Tutorial.


from operator import index
from sqlite3 import Cursor
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from grpc import StatusCode
from httpx import post
from pydantic import BaseModel
from typing import List, Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql import text

from . import models, schemas, utils
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




while True:
    # Hard Coding the Passwords and all are generally not advisable.
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'FastAPI', user = 'postgres', password = 'dipasha321', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was Successfull !!")
        break
    except Exception as error:
        print("Database Connection was Failed !")
        print("Error : ", error)
        time.sleep(2)





@app.get("/")
async def root():
    return {"message": "My Name is Racheet Anand and I am the ruler of this world."}


# Posts Path Operations


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    print(post)
    return post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    print(id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found.")
    print("\n\n", type(post), "\n\n")
    print("\n\n", (post), "\n\n")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.put("/posts/{id}")
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    print(new_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    post_query.update( new_post.model_dump() , synchronize_session = False)
    db.commit()
    return {"Message": f"Updated the Post of ID {id}",
            "Updated Post": post_query.first()}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    post.delete(synchronize_session = False)
    db.commit()
    print("\n\n", type(post), "\n\n")
    print("\n\n", post, "\n\n")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Users Path Operations


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    print(id)
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with ID: {id} was not found.")
    print("\n\n", type(user), "\n\n")
    print("\n\n", (user), "\n\n")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_posts(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user.model_dump())
    # Hash the password - user.hashed_password
    user.hashed_password = utils.hash(user.hashed_password)
    new_user = models.User(**user.model_dump())
    # new_user = models.User(title=user.title, content=user.content, published=user.published)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


