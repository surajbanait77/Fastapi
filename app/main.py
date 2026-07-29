# from sqlalchemy.orm import Session
# from fastapi.params import Body # Means: "it tells fastapi "Take this value from the request body."
# from random import randrange 
from fastapi import FastAPI #,Response,HTTPException,status,Depends,APIRouter
from . import Model
from .Database import engine #, SessionLocal ,get_db 
from .schemas import PostBase, PostCreate, Post, UserCreate ,UserOut
from .import utils  # 💀
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

from .config import settings

print(settings.database_username)

# Model.Base.metadata.create_all(bind=engine) # it create all of the models

app=FastAPI()

origins=['*']

app.add_middleware( # for CORS policy that the server can get request from multiple domain rather than the same domain as api's
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)        
app.include_router(user.router)        
app.include_router(auth.router)        
app.include_router(vote.router)        



print=(settings.database_username)








































# my_posts=[{"Title":"title of the post 1", "Content":"contetn of the post 1","id":1},{"Title":"MLBB", "Content":"MPL","id":2}]

# def find_posts(id):  # NEEDED BEFORE DB
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i



# for testing of sqlalchemy
# @app.get("/sqlalchemy") # creates a database session 
# def test_posts(db: Session = Depends(get_db)):
#      posts=db.query(Model.Post).all()
#      return {"Data": posts}





'''Basic path operation to check working '''
@app.get("/")
async def root():
    return {"message": "Hello World!!!!!!!!!!!!!"}

# @app.get("/posts")
# async def root():
#     return {"Data":"New_posts"}


# @app.post("/createposts")  # to get the req body and print it
# async def create_post(a: dict=Body(...)):
#     print(a)
#     return {"new_post": f"title:{a["title"]} , content:{a["content"]}"} 


# for validation checking 
# @app.post("/posts")
# async def create_post(post: Post):
#     return {"Data": post.dict()}

''' ~ ~ ~ XXXX  ~ ~ ~'''


















