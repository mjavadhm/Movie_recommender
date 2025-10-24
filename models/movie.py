from typing import List, Optional
from datetime import date

from sqlalchemy import Integer, String, Text, Float, BigInteger, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin
from .associations import (
    movie_genre_association,
    movie_keyword_association,
    movie_company_association,
    movie_country_association,
    movie_language_association,
    movie_provider_association,
)


class Movie(Base, TimestampMixin):
    """Movie model - Main entity"""
    
    __tablename__ = 'movies'
    
    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    
    # Basic Information
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    original_title: Mapped[str] = mapped_column(String(500), nullable=False)
    original_language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    # Descriptive Fields
    overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tagline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Dates
    release_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)
    
    # Media Paths
    poster_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    backdrop_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Numeric Data
    runtime: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # minutes
    budget: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)  # USD
    revenue: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)  # USD
    
    # Ratings & Popularity
    vote_average: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    vote_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    popularity: Mapped[Optional[float]] = mapped_column(Float, nullable=True, index=True)
    
    # Status & Additional Info
    status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Released, Post Production, etc.
    adult: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    video: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    homepage: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    imdb_id: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    
    # Foreign Keys
    collection_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )
    
    # ==================== RELATIONSHIPS ====================
    
    # Collection
    collection: Mapped[Optional["Collection"]] = relationship(
        "Collection",
        back_populates="movies",
        foreign_keys=[collection_id],
        lazy="selectin",
    )
    
    # Many-to-Many: Genres
    genres: Mapped[List["Genre"]] = relationship(
        "Genre",
        secondary=movie_genre_association,
        back_populates="movies",
        lazy="selectin",
    )
    
    # Many-to-Many: Keywords
    keywords: Mapped[List["Keyword"]] = relationship(
        "Keyword",
        secondary=movie_keyword_association,
        back_populates="movies",
        lazy="selectin",
    )
    
    # Many-to-Many: Production Companies
    production_companies: Mapped[List["ProductionCompany"]] = relationship(
        "ProductionCompany",
        secondary=movie_company_association,
        back_populates="movies",
        lazy="selectin",
    )
    
    # Many-to-Many: Production Countries
    production_countries: Mapped[List["ProductionCountry"]] = relationship(
        "ProductionCountry",
        secondary=movie_country_association,
        back_populates="movies",
        lazy="selectin",
    )
    
    # Many-to-Many: Spoken Languages
    spoken_languages: Mapped[List["SpokenLanguage"]] = relationship(
        "SpokenLanguage",
        secondary=movie_language_association,
        back_populates="movies",
        lazy="selectin",
    )
    
    # Many-to-Many: Providers
    providers: Mapped[List["Provider"]] = relationship(
        "Provider",
        secondary=movie_provider_association,
        back_populates="movies",
        viewonly=True,
    )
    
    # Cast (Actors)
    cast: Mapped[List["Person"]] = relationship(
        "Person",
        secondary="movie_cast_association",
        back_populates="movies_as_cast",
        viewonly=True,
    )
    
    # Crew (Directors, Writers, etc.)
    crew: Mapped[List["Person"]] = relationship(
        "Person",
        secondary="movie_crew_association",
        back_populates="movies_as_crew",
        viewonly=True,
    )
    
    # One-to-Many: Videos
    videos: Mapped[List["Video"]] = relationship(
        "Video",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    # One-to-Many: Release Dates
    release_dates: Mapped[List["MovieReleaseDate"]] = relationship(
        "MovieReleaseDate",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    # One-to-Many: User Ratings
    user_ratings: Mapped[List["UserMovieRating"]] = relationship(
        "UserMovieRating",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<Movie(id={self.id}, title='{self.title}', year={self.release_date.year if self.release_date else 'N/A'})>"