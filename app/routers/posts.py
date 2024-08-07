from .. import models, schemas, oauth2
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db

# Posts Path Operations

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
# def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): # Query Parameter
    # print("The User ID is : ", user_id, "\n\n") # Back when It used to return the token data from get_current_user
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    print(f"\nThe Limit is : {limit}, The Skip is : {skip}, The Search Keyword is : \"{search}\"\n")
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    # print(results)
    results = results.filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    results = results.all()
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # If we want to make a notes making app and not share all the notes to the public.
    return results
    return results.all()
    return posts


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    print(post)
    return post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    print("Get Post ID is : ", id)
    post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post, func.count(models.Vote.user_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    results = results.filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found.")
    # print("\n\n", type(post), "\n\n")
    # print("\n\n", (post), "\n\n")
    return results
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    print(post.model_dump())
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}")
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    print(new_post)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised to perform requested Action.")
    post_query.update( new_post.model_dump() , synchronize_session = False)
    db.commit()
    return {"Message": f"Updated the Post of ID {id}",
            "Updated Post": post_query.first()}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"The Post with ID {id} was not found.")
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorised to perform requested Action.")
    post_query.delete(synchronize_session = False)
    db.commit()
    print("\n\n", type(post), "\n\n")
    print("\n\n", post, "\n\n")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

