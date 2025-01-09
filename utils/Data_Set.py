# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    movieId = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)

    def __repr__(self):
        return f"<Movie(movieId={self.movieId}, title='{self.title}')>"
