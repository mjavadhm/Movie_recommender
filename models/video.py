from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class Video(Base, TimestampMixin):
    """Video model for trailers and clips"""
    
    __tablename__ = 'videos'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('movies.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    tmdb_video_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    key: Mapped[str] = mapped_column(String(255), nullable=False)  # YouTube key
    site: Mapped[str] = mapped_column(String(50), nullable=False)  # YouTube, Vimeo, etc.
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # Trailer, Teaser, Clip, etc.
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 360, 720, 1080
    official: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="videos")
    
    def __repr__(self) -> str:
        return f"<Video(id={self.id}, type='{self.type}', name='{self.name}')>"


class MovieReleaseDate(Base, TimestampMixin):
    """Movie release date model (per country)"""
    
    __tablename__ = 'movie_release_dates'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('movies.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    release_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    certification: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # PG-13, R, etc.
    release_type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1=Premiere, 2=Limited, 3=Theatrical, etc.
    
    # Relationships
    movie: Mapped["Movie"] = relationship("Movie", back_populates="release_dates")
    
    def __repr__(self) -> str:
        return f"<MovieReleaseDate(movie_id={self.movie_id}, country='{self.country_code}')>"