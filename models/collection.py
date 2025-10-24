from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class Collection(Base, TimestampMixin):
    """Movie collection model (e.g., Marvel Cinematic Universe)"""
    
    __tablename__ = 'collections'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    poster_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    backdrop_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    overview: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        back_populates="collection",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<Collection(id={self.id}, name='{self.name}')>"