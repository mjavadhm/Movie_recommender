
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    
    user_identifier = Column(String(255), unique=True, nullable=False, index=True) 
    
    
    ratings = relationship("UserMovieRating", back_populates="user", cascade="all, delete-orphan")