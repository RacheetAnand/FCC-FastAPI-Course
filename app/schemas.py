# We only need Schemas when Creating or Updating a Post.

from datetime import datetime, time
from typing import Optional
# import datetime
from pydantic import BaseModel, EmailStr, conint


# Schema for Users

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    hashed_password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    # created_at: time
    # is_active: bool
    # items: list[Item] = []

    class Config:
        from_attributes = True
        # orm_mode = True

class UserLogin(UserBase):
    hashed_password: str


# Schema for Tokens

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



# Schema for Posts

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Schema for giving the response back.

class Post(PostBase):
    id: int
    created_at: datetime
    # created_at: time
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True
        # orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
        # orm_mode = True


# Schema for Votes

class Vote(BaseModel):
    post_id: int
    # dir: 0 | 1
    # dir: int(0) | int(1)
    dir: conint(le=1) # Gotta find a better way of doing this.


class FoundVote(BaseModel):
    post_id: int
    user_id: int
    user: UserOut
    post: Post

class VoteOut(BaseModel):
    message: str
    Found_Vote: FoundVote
    # User_Email: 
    class Config:
        from_attributes = True







# class TokenData(BaseModel):
#     username: str | None = None


# class Post(BaseModel):
#     id: int
#     title: str
#     content: str
#     published: bool
#     created_at: time
#     # created_at: datetime.time
#     # created_at: datetime # I don't know why but it does not work as it did in the tutorial.

#     # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict, but an ORM model (or any other arbitrary object with attributes).
#     # Link -> https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode
#     class Config:
#         orm_mode = True

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None