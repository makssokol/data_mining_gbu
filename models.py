from enum import unique
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql.schema import Table

Base = declarative_base()


tag_post = Table('tag_post', Base.metadata,
    Column('post_id', Integer, ForeignKey('post.id')),
    Column('tag_id', Integer, ForeignKey('tag.id')))


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, unique=False, nullable=False)
    first_img = Column(String, nullable=True, unique=False)
    date_time = Column(DateTime, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')
    tags = relationship("Tag", secondary=tag_post)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, unique=False, nullable=False)
    posts = relationship('Post')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    tag_url = Column(String, nullable=False, unique=True)
    name = Column(String, unique=False, nullable=False)



