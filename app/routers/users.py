from .. import models, schemas, utils
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

# Users Path Operations

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    print(id)
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID: {id} was not found.")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user.model_dump())
    # Hash the password - user.hashed_password
    user.hashed_password = utils.hash(user.hashed_password)
    new_user = models.User(**user.model_dump())
    # new_user = models.User(title=user.title, content=user.content, published=user.published)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

