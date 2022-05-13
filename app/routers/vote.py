from socket import AI_ADDRCONFIG
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import oauth2,schemas,models,database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(database.get_db), current_user =  Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    #checking if vote is happening on post which does not exists
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {vote.post_id} does not exist")    

    
    vote_query= db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id ==current_user.id)
    
    found_vote=vote_query.first()
    #to check if post has been already voted by same user 
    if (vote.dir ==  1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id=vote.post_id, user_id =current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully voted"}

    else:
        #check if user is trying do delete like post which already been disliked
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"}
