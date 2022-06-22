from typing import List
from blog.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


#metadata = sqlalchemy.MetaData()

class Blog(Base):
    __tablename__ = "blog"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    
    comments = relationship("Comments", back_populates="blog")

class Comments(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    blog_id = Column(Integer, ForeignKey("blog.id"))
    
    blog = relationship("Blog", back_populates="comments")
    
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    
    
    
    
    
    
    
