from fastapi import status, Depends, APIRouter, HTTPException
from .. import schemas, models, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",    
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post.id} does not exist")

    """
    check to see if user already liked a post by validating from Vote table, if
    the post_id and user_id being submitted already exist in the Vote table
    """
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    # pulling dir from vote schema
    # vote.dir == 1 means user initiates a post like
    if (vote.dir == 1):
        # if post already liked by current user raise error/already in Vote table
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already voted on post {vote.post_id} ")
        # vote not found in post table
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        # if vote exists, delete it
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted vote"}




