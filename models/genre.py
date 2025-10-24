from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class Genre(Base, TimestampMixin):
    """Genre model (Drama, Action, Comedy, etc.)"""
    
    __tablename__ = 'genres'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_genre_association",
        back_populates="genres",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<Genre(id={self.id}, name='{self.name}')>"