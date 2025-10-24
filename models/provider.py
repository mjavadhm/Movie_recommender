from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class Provider(Base, TimestampMixin):
    """Watch provider model (Netflix, Disney+, etc.)"""
    
    __tablename__ = 'providers'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_provider_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_provider_association",
        back_populates="providers",
        viewonly=True,
    )
    
    def __repr__(self) -> str:
        return f"<Provider(id={self.id}, name='{self.name}')>"