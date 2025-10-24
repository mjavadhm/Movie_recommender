from typing import TYPE_CHECKING, List, Optional
from datetime import date

from sqlalchemy import Integer, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class Person(Base, TimestampMixin):
    """Person model for cast and crew"""
    
    __tablename__ = 'persons'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    
    # Optional fields
    biography: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    deathday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    place_of_birth: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    profile_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    known_for_department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    gender: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0=unknown, 1=female, 2=male
    popularity: Mapped[Optional[float]] = mapped_column(nullable=True)
    
    # Relationships
    movies_as_cast: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_cast_association",
        back_populates="cast",
        viewonly=True,
    )
    
    movies_as_crew: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_crew_association",
        back_populates="crew",
        viewonly=True,
    )
    
    def __repr__(self) -> str:
        return f"<Person(id={self.id}, name='{self.name}')>"