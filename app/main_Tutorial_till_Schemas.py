# uvicorn app.main:app --reload
# Removing all the Note Comments from the Tutorial.

from operator import index
from sqlite3 import Cursor
# from turtle import pos
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from grpc import StatusCode
from httpx import post
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.sql import text

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

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


my_posts = [
    {'title': 'Title of Post 1', 'content': 'Check out these awsome Beaches.', 'published': False, 'rating': 4, 'id': 1}, 
    {'title': 'Title of Post 2', 'content': 'Check out these awsome Beaches.', 'published': False, 'rating': 4, 'id': 2}
            ]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
    return None

def find_index_of_post(id: int):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i, post
    return -1, None


@app.get("/")
async def root():
    return {"message": "My Name is Racheet Anand and I am the ruler of this world."}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post) # This is Just a Unrun SQL Query
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    print(posts)
    return {"Data": posts}
    # return {"Status": "Success"}



@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"Data": posts}


@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    # Three Methods to do the same thing, Link -> https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending?answertab=scoredesc#tab-top
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    # post = db.query(models.Post).order_by(desc(models.Post.created_at)).first()
    # post = db.query(models.Post).order_by(text("""created_at DESC""")).first()
    print(post)
    return {"Latest Post Details": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    print(id)
    # cursor.execute("""SELECT * FROM public.posts WHERE id = %s;""", (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found.")
    print("\n\n", type(post), "\n\n")
    print("\n\n", (post), "\n\n")
    return {"Post Details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # print("\n\n", type(new_post.__dict__), "\n\n")
    # print("\n\n", type(new_post.__class__), "\n\n")
    # print(new_post.__dict__, "\n\n")
    # print(new_post.__class__, "\n\n")
    # print("\n\n", type(new_post.__annotations__), "\n\n")
    # print(new_post.__annotations__, "\n\n")
    return {"data": f"{new_post}"}
            # "ID": post['id'],
            # "Header": post['title'],
            # "Content": post['content']}


@app.put("/posts/{id}")
def update_post(id: int, new_post: Post, db: Session = Depends(get_db)):
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


