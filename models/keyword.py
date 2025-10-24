from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class Keyword(Base, TimestampMixin):
    """Keyword model for movie tagging"""
    
    __tablename__ = 'keywords'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_keyword_association",
        back_populates="keywords",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<Keyword(id={self.id}, name='{self.name}')>"