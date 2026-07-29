# purpose: without using pgadmin we can create table with python module.

# "SQLAlchemy lets us interact with the database using Python code,
#     and it automatically generates the SQL queries required by PostgreSQL."
from .Database import Base
from sqlalchemy import Column, Integer, String, Boolean # for creating column
from sqlalchemy import null ,TIMESTAMP,text
from sqlalchemy import ForeignKey 
from sqlalchemy.orm import relationship



class Post(Base):
    __tablename__="posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String ,nullable=False)
    published = Column(Boolean ,server_default='True', nullable=True)
    created_on=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship("User")
    

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String ,nullable=False)
    created_on=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # posts = relationship("Post")


class Vote(Base):
    __tablename__="votes"

    user_id=Column(Integer ,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer ,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
