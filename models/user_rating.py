
from sqlalchemy import Column, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func

class UserMovieRating(Base):
    __tablename__ = 'user_movie_ratings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Float, nullable=False) 
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")