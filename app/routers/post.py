
from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import Optional,List # Means: "This value can either be a specific type OR None."
from ..import Model ,schemas,oauth2
from ..schemas import UserCreate, UserOut,PostCreate
from ..Database import get_db
from ..schemas import Post, PostOut
from sqlalchemy import func




router = APIRouter(
 prefix ="/posts",
 tags=["posts"]
)




'''~ ~ ~ ORM SPECIFIC ~ ~ ~'''


'''To get all post'''

# @router.get("/",response_model=List[Post]) #to pass query from server to postgres spl 
@router.get("/", response_model=List[PostOut]) #to pass query from server to postgres spl 
async def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int=10, skip:int = 0, search:Optional[str]=''):
    posts=db.query(Model.Post).limit(limit).offset(skip).all()
   # posts=db.query(Model.Post).filter(Model.Post.user_id == current_user.id).all()  # for geting specific user post
    
    post=db.query(Model.Post,func.count(Model.Vote.post_id).label("votes")
            ).join(Model.Vote,Model.Vote.post_id == Model.Post.id, isouter=True).group_by(Model.Post.id).filter(Model.Post.user_id == current_user.id).all()
    
    return post




'''To create a post'''

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=Post) # It assigns a unique id to new post & print it also, it will append that id to the get(posts) from which we can access all posts
async def create_post(post: PostCreate , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # new_posts= Model.Post(title=post.title, content=post.content , published=post.published)
    print(current_user)
    new_posts= Model.Post( user_id=current_user.id,**post.dict())
    db.add(new_posts) #save the object.
    db.commit()  # saves in DB
    db.refresh(new_posts) #to get the latest version of this row.( Get updated data from database)"
    return new_posts





'''To get specific post'''

@router.get("/{id}",response_model=PostOut)  
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(Model.Post).filter(Model.Post.id == id).first()

    post=db.query(Model.Post,func.count(Model.Vote.post_id).label("votes")
                ).join(Model.Vote,Model.Vote.post_id == Model.Post.id, isouter=True).group_by(Model.Post.id).filter(Model.Post.id == id).first()
 

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} was not found!!!")
    if post.user_id != current_user.id:
                     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post




'''To delete a post'''
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(Model.Post).filter(Model.Post.id == id)

    post= post_query.first()

    print("Current User ID:", current_user.id)
    print("Post:", post)
    if post ==  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id:{id} dosn't exist !!")

    if post.user_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)







'''To update a post'''
@router.put("/{id}",response_model=Post)
def update_post(id: int, updated_post:PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
        
        post_query = db.query(Model.Post).filter(Model.Post.id == id)
        post = post_query.first()
       
        if post == None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                 detail=f"post with id:{id} dosn't exist !!")
        post_query.update(updated_post.dict(), synchronize_session=False)

        if post.user_id != current_user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        db.commit()

        return post_query.first()



''' ~ ~ ~ XXXX ~ ~ ~ '''









'''~ ~ ~ For Local DB ~ ~ ~'''

'''To get all posts'''
# @app.get("/posts")        
# async def get_post():
#     return {"Data":my_posts}


'''To create post''' 
# @app.post("/posts", status_code=status.HTTP_201_CREATED) # It assigns a unique id to new post & print it also, it will append that id to the get(posts) from which we can access all posts
# async def create_post(post: Post):
#     post_dict=post.dict()
#     post_dict['id'] = randrange(0,100000) 
#     my_posts.append(post_dict)
#     return {"Data": post_dict}


'''To get latest post'''
# @app.get("/posts/latest")  #***This should be placed before get_post func else it took "latest" as id=int through error***
# def get_latest_post():
#     post=my_posts[len(my_posts)-1]
#     return {"Detail":post}



'''To get specific post'''
# @app.get("/posts/{id}")  # Mistake: Both id must have same type int(id)
# def get_post(id: int):
#      post=find_posts(id)
#      if not post:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             details=f"post with id:{id} was not found!!!")
#      return{"post_detail":post}



'''To delete post'''
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     index=find_index_post(id)

#     if index == None :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"post with id:{id} does not exists")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



'''To update post'''
# @app.put("/posts/{id}")
# def update_post(id: int, post:Post):
#            index=find_index_post(id)

#            if index ==  None:
#               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                                  detail=f"post with id:{id} dosn't exist !!")
           
#            post_dict=post.dict()
#            post_dict['id']=id
#            my_posts[index]=post_dict
#            return {"Data": post_dict}

''' ~ ~ ~ XXXX ~ ~ ~ '''




'''After DB'''

'''To get all post'''
# @app.get("/posts") #to pass query from server to postgres spl 
# async def get_post():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"Data": posts}



'''To create post'''
# @app.post("/posts", status_code=status.HTTP_201_CREATED)  # It assigns a unique id to new post & print it also, it will append that id to the get(posts) from which we can access all posts
# async def create_post(post: Post):
#    # cursor.execute(f"INSERT INTO posts(title,content,published) VALUES ({post.title}, {post.content},{post.published})") 💉# SQL INJECTION point
'''({post.title}, {post.content},{post.published}) -> this will lead to sql injection
bcoz user can put sql command as input will allow them to manipulate the DB directly which is refered as SQL INJECTION'''
#     cursor.execute('''INSERT INTO posts(title,content,published) 
#                       VALUES (%s,%s,%s)
#                       RETURNING *''',(post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}




'''To get specific post'''
# @app.get("/posts/{id}")  
# def get_post(id: int):
#      cursor.execute('''SELECT * FROM posts 
#                        WHERE id = %s''',(str(id)))
#      post = cursor.fetchone()
#      if not post:
#          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id:{id} was not found!!!")
#      return{"post_detail":post}



'''To delete a post'''
# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) 
# def delete_post(id: int):
#     cursor.execute('''DELETE FROM posts 
#                       WHERE id = %s
#                       returning *''' , str(id))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post ==  None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id:{id} dosn't exist !!")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)




'''To update a post'''
# @app.put("/posts/{id}")
# def update_post(id: int, post:Post):
           
#         cursor.execute('''UPDATE posts SET title=%s, content=%s, published=%s
#                           WHERE id = %s
#                           RETURNING *''',
#                                          (post.title,post.content,post.published,str(id,)))
#         updated=cursor.fetchone()
#         conn.commit()

#         if updated == None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                                  detail=f"post with id:{id} dosn't exist !!")
#         return {"Data": updated }

''' ~ ~ ~ XXXX ~ ~ ~ '''





