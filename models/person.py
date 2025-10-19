
from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.orm import relationship
from . import Base

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(Text, nullable=False)
    profile_path = Column(String(255)) 
    known_for_department = Column(Text)

    
    cast_movies = relationship("MovieCast", back_populates="person")
    crew_movies = relationship("MovieCrew", back_populates="person")