# For the Terminal Notes we can actually use the "uvicorn main:app" we have to manually always rerun the code and relod the webpage on the browser so we can use it as we change the codebase. for the solution to this problem is actually to just use command "uvicorn main:app --reload"

from operator import index
from turtle import pos
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body
from grpc import StatusCode
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Optional Methods Having Default Values which can or cannot be send when using the POST Operations.
    rating: Optional[int] = None # Optional Methods not Having Default Values which can or cannot be send when using the POST Operations.

while True:
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
# requests GET method url: "/"

@app.get("/") # <-- this is the path where the we have to go to the refrence to the main server url to see the results of it, the funtion we have written. ##### .get() is the method and "/" is the path and root() is the function. And from the @symbol we get our decorator.
async def root(): # we just for the sake of specifying the function named it async keyword. and the root() is just the general name of the function and it is advisable to make it descripive of the thing it actually does.
    return {"message": "My Name is Racheet Anand and I am the ruler of this world."}
    # return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    # return {"data": "This is your posts."}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # def create_posts(payload: dict = Body(...)): #We need to want to define a schema which we can then force our clients to send and which we can validate.
def create_posts(post: Post):
    print(post.model_dump())
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    print(post_dict)
    my_posts.append(post_dict)
    # print(post)
    # print(post.dict())
    # print(post.model_dump_json())
    return {"data": f"{post_dict}",
            "Header": f"{post.title}",
            "message": f"{post.content}"}
    # return {"post": f"title => {post['title']}; content => {post['content']}", "message": "Successfully Created posts."}
    # return {"message": "Successfully Created posts."}

@app.get("/posts/latest") # Always Make Sure that when you are making a new path with the same application of CRUD then the first one written will be executed. 
def get_latest_post(): # Always remember when structuring the API that Path variables can get us in trouble.
    post = my_posts[-1]
    print(post)
    return {"Latest Post Details": post}

@app.get("/posts/{id}") # this {id} is referred to as a Path Parameter.
def get_post(id: int, response: Response): # Here we are giving the part of checking and converting the string type of the id to the int type to FastAPI
    print(id)
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found.")
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with ID: {id} was not found."}
    return {"Post Details": post}
    # return {"Post Details": f"Here is the Post {id} that you are looking for."}
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index, post = find_index_of_post(int(id))
    print("The Index is : ", index,"\nAnd the Post is : ", post)
    if post is not None:
        my_posts.pop(index)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"Message": f"The Post of ID {id} was Successfully deleted.", # As when we do 204 we are not allowed to send a response to the client.
    #         "Index": index,
    #         "Post Contents": post}
@app.put("/posts/{id}")
def update_post(id: int, new_post: Post):
    print(new_post)
    index, old_post = find_index_of_post(int(id))
    print("The Index is : ", index,"\nAnd the Post is : ", old_post)
    if old_post is not None:
        post_dict = new_post.model_dump()
        post_dict['id'] = id
        my_posts[index] = post_dict
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    return {"Message": f"Updated the Post of ID {id}",
            "Old Post": old_post,
            "New Post": post_dict}













# CRUD => 
# + Create -> (POST), 
# + Read -> (GET{ID}/GET), 
# + Update -> (PUT [If you want to change the entire thing and all the fields required must be filled] /PATCH [If you want to change the specific field in the thing] ), 
# + Delete -> (DELETE).