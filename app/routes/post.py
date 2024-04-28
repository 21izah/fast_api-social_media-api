

from typing import Any, Dict, List, Optional

from fastapi import Response, status, HTTPException, Depends, utils,APIRouter

from ..import models

from sqlalchemy.orm import Session
from sqlalchemy import func

from ..import  models
from ..database import  get_db
from ..import schemas, utils,oauth2

router = APIRouter(
  prefix="/api/posts" 
)



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(postModel: schemas.PostCreate, db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):

    # new_post = models.Post(title=postModel.title,content=postModel.content,published= postModel.published)
    new_post = models.Post(owner_id =current_user.id,**postModel.dict())
    print(current_user.id )
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #return the new post
    return new_post


@router.get("/",response_model=List[schemas.Post])
async def get_post(db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    posts = db.query(models.Post).all()
    # results= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    print(current_user.id)
    print(type(posts))
    
    return posts
  
  
@router.get("/user")
# @router.get("/user",response_model=List[schemas.PostOut])
async def get_post(db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int = 10, skip:int=0, search:Optional[str]="" ):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id,models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(type(results))
    # post_instances = [post for post, _ in results]

    # return post_instances
    combined_data: List[Dict[str, Any]] = []

    # Iterate over the results
    for post, votes in results:
        # Convert each post and its vote count to a dictionary
        post_dict = {
            "id": post.id,
            "title":post.title,
            "content":post.content,
            "published":post.published,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            # Add other attributes as needed
            "votes": votes
        }
        # Append the combined data to the list
        combined_data.append(post_dict)

    return {"data":combined_data}
    # return (results)
    # return posts

@router.get("/{id}")
async def get_post(id,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn't exist")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requestde action")
    return post
    

@router.delete("/{id}")
def delete_post(id,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn't exist")
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requestde action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
async def update_post(postModel: schemas.PostCreate, id,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesn't exist")
    if updated_post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    
    post_query.update(postModel.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()