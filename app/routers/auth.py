from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .. import schemas, models, database, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # OAuth2PasswordRequestForm returns a dictionary having keys as username and password.
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.hashed_password):
    # if not utils.verify(user_credentials.hashed_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")


    access_token = oauth2.create_access_token(data={"user_id": user.id} )
    return {"access_token": access_token, "token_type": "bearer"}
    # return Token(access_token=access_token, token_type="bearer")
    # return {"Token": "Example Token"}