
from sqlalchemy import Column, Integer, Text, Date, Float, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    tmdb_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(Text, nullable=False)
    original_title = Column(Text)
    overview = Column(Text)
    tagline = Column(Text)
    release_date = Column(Date)
    runtime = Column(Integer)  
    budget = Column(BigInteger)
    revenue = Column(BigInteger)
    popularity = Column(Float)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    
    
    poster_path = Column(String(255))
    backdrop_path = Column(String(255))
    
    imdb_id = Column(String(50), unique=True, index=True)
    status = Column(String(50)) 
    original_language = Column(String(10))

    
    
    
    collection_id = Column(Integer, ForeignKey('collections.id', ondelete="SET NULL"))
    collection = relationship("Collection", back_populates="movies")
    
    
    genres = relationship("Genre", secondary="movie_genre_association", back_populates="movies")
    keywords = relationship("Keyword", secondary="movie_keyword_association", back_populates="movies")
    production_companies = relationship("ProductionCompany", secondary="movie_company_association", back_populates="movies")
    production_countries = relationship("ProductionCountry", secondary="movie_country_association", back_populates="movies")
    spoken_languages = relationship("SpokenLanguage", secondary="movie_language_association", back_populates="movies")

    
    videos = relationship("Video", back_populates="movie", cascade="all, delete-orphan")
    release_dates = relationship("MovieReleaseDate", back_populates="movie", cascade="all, delete-orphan")
    watch_providers = relationship("MovieWatchProvider", back_populates="movie", cascade="all, delete-orphan")

    
    cast = relationship("MovieCast", back_populates="movie", cascade="all, delete-orphan")
    crew = relationship("MovieCrew", back_populates="movie", cascade="all, delete-orphan")

    
    ratings = relationship("UserMovieRating", back_populates="movie", cascade="all, delete-orphan")