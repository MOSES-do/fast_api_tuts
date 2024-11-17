from pydantic import BaseModel, EmailStr, Field
from datetime  import datetime
from typing import Optional, List, Annotated



class PostBase(BaseModel):
    """post response object"""
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

class UserCreate(BaseModel):
    email: EmailStr
    password: str    




# pydantic response object for FastAPI
class UserOut(BaseModel):
    id:int
    email: str
    created_at: datetime
    # posts: List[PostBase] display post related to a user in user response object
    # SQLAlchemy model below converts it to a regular pydantic model/dict before sending it as a response
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(PostBase):
    id: int 
    created_at: datetime
    owner_id: int
    # possible becos of the sqlalchemy relationship between two tables/classes (Post and User)
    owner: UserOut
    
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes:int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    # Adding constraints to fields
    dir: Annotated[int, Field(ge=0, le=1)]
