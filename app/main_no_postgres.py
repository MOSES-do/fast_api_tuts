from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Saving posts in memory
my_posts = [{"title":"title of post 1", "content": "content of post 1", "id":1}, {"title":"Fav Food", "content": "I like pizza", "id":2}]

@app.get("/")
async def root():
    return {"message":"Hello World!!!!!"}

@app.get("/posts")
def get_posts():
    # 
    return {"data":my_posts}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    # enumerate returns the index of the post with id...
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # convert post to a python dictionary using model_dump()
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_posts():
    # return last post
    post = my_posts[len(my_posts)-1]
    return {"details": post}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    # convert received post to dictionary
    post_dict = post.model_dump()
    # attach an id
    post_dict['id'] = id
    # replace new post with post at index
    my_posts[index] = post_dict
    return {'message':'updated post'}
    








