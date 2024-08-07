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

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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
    # if db_user is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    return {"Status": "Success"}



@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM public.posts;""")
    posts = cursor.fetchall()
    print("\n\n", posts, "\n\n")
    # print("\n\n", posts[0]['id'], "\n\n") # New Stuff Learned.
    # print("\n\n", posts[1], "\n\n")
    
    # I Copied this from Stackoverflow Link -> https://stackoverflow.com/questions/21158033/query-from-postgresql-using-python-as-dictionary -- Gotta Learn more from this Page.
    # # query
    # cursor.execute("SELECT * FROM myTable")

    # # transform result
    # columns = list(cursor.description)
    # result = cursor.fetchall()

    # # make dict
    # results = []
    # for row in result:
    #     row_dict = {}
    #     for i, col in enumerate(columns):
    #         row_dict[col.name] = row[i]
    #     results.append(row_dict)

    # # display
    # print(result)
    return {"data": posts}
    # return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM public.posts ORDER BY created_at DESC LIMIT 1;""")
    post = cursor.fetchone()
    print(post)
    return {"Latest Post Details": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    cursor.execute("""SELECT * FROM public.posts WHERE id = %s;""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found.")
    print("\n\n", type(post), "\n\n")
    print("\n\n", (post), "\n\n")
    return {"Post Details": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO public.posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published)) # This is not vulnerable to SQL Injection Attacks as the placeholders & functions can sanitize those SQL Strings
    # cursor.execute(f"INSERT INTO public.posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})") # This is Vulnerable to SQL Injection Attacks
    post = cursor.fetchone()
    conn.commit()
    print("\n\n", type(post), "\n\n")
    print(post, "\n\n")
    return {"data": f"{post}",
            "ID": post['id'],
            "Header": post['title'],
            "Content": post['content']}


@app.put("/posts/{id}")
def update_post(id: int, new_post: Post):
    print(new_post)
    cursor.execute("""UPDATE public.posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (new_post.title, new_post.content, new_post.published, str(id)))
    new_post = cursor.fetchone()
    if new_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    conn.commit()
    return {"Message": f"Updated the Post of ID {id}",
            "Updated Post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM public.posts WHERE id = %s RETURNING *;""", (str(id),))
    post = cursor.fetchone()
    print("The Created Time is : ", post['created_at'],"\nAnd the Post is : ", post)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    conn.commit()
    print("\n\n", type(post), "\n\n")
    print("\n\n", post, "\n\n")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


