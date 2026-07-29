'''> Schema/ pydantic model define the structure of a request and response 
   > This will ensure that when a user create a post the request will only go 
     through a proper structure of code which will provide user details like title, content ,id'''


from pydantic import BaseModel ,EmailStr,Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# for validation that input is correct or not ("BaseModel": checks that the data sent to your API is valid.)
class PostBase(BaseModel):
      title: str
      content: str
      published: bool | None=True
    #   rating: Optional[int]=None

class PostCreate(PostBase):
      pass

class UserOut(BaseModel):
      id : int
      email: EmailStr
      created_on : datetime

      class Config:
            orm_model = True

class Post(PostBase):
      id: int
      created_on: datetime
      user_id: int
      user:UserOut


      class Config:
            orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True   
        
class UserCreate(BaseModel):
       email: EmailStr
       password: str



class UserLogin(BaseModel):
      email: EmailStr
      password: str


class Token(BaseModel):
      access_token: str
      token_type: str

class TokenData(BaseModel):
      id: Optional[int] = None

class Vote(BaseModel):
      post_id: int
      dir: int=Field(Le=1)