from grpc import StatusCode
from .. import models, schemas, oauth2
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

# Posts Path Operations

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)



@router.post("/", status_code=status.HTTP_201_CREATED)
            #  , response_model=schemas.VoteOut)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print("The Current User ID is : ", current_user.id)
    print("The Current User Email is : ", current_user.email, "\n")
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        print(f"Post with ID: {vote.post_id} was not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {vote.post_id} was not found.")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            print(f"The User of ID : {current_user.id} has already voted on the Post of ID : {vote.post_id}")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The User of ID : {current_user.id} has already voted on the Post of ID : {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        found_vote = vote_query.first()
        # vote_out: schemas.VoteOut = {"message": f"The Vote of User of ID : {current_user.id} is added on the Post of ID : {vote.post_id}", "Found_Vote": found_vote}
        # vote_out = {"message": f"The Vote of User of ID : {current_user.id} is added on the Post of ID : {vote.post_id}", "Found_Vote": found_vote}
        # return {"message": f"The Vote of User of ID : {current_user.id} is added on the Post of ID : {vote.post_id}"}
        # return vote_out
        print(f"The Vote of User of ID : {current_user.id} is added on the Post of ID : {vote.post_id}")
        return {"message": f"The Vote of User of ID : {current_user.id} is added on the Post of ID : {vote.post_id}",
                "Found_Vote": found_vote,
                "User": found_vote.user,
                "Post": found_vote.post}
    elif vote.dir == 0:
        if not found_vote:
            print(f"The User of ID : {current_user.id} has NOT voted on the Post of ID : {vote.post_id}. And So it Does Not Exist")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The User of ID : {current_user.id} has NOT voted on the Post of ID : {vote.post_id}. And So it Does Not Exist")
        # found_vote = vote_query.first()
        # vote_out: schemas.VoteOut
        # vote_out = {"message": f"The Vote of User of ID : {current_user.id} is REMOVED from the Post of ID : {vote.post_id}", "Found_Vote": found_vote}
        vote_query.delete(synchronize_session = False)
        db.commit()
        print(f"The Vote of User of ID : {current_user.id} is REMOVED from the Post of ID : {vote.post_id}")
        return {"message": f"The Vote of User of ID : {current_user.id} is REMOVED from the Post of ID : {vote.post_id}"}
        # return {"message": f"The Vote of User of ID : {current_user.id} is REMOVED from the Post of ID : {vote.post_id}",
        #         "Found_Vote": found_vote}
    else:
        print("The Vote Direction was neither 1 or 0. HTTP_400_BAD_REQUEST . The Vote Direction is Not Properly Defined.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The Vote Direction is Not Properly Defined.")