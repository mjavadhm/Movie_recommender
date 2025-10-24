from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .movie import Movie


class ProductionCompany(Base, TimestampMixin):
    """Production company model"""
    
    __tablename__ = 'production_companies'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tmdb_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    origin_country: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_company_association",
        back_populates="production_companies",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<ProductionCompany(id={self.id}, name='{self.name}')>"


class ProductionCountry(Base, TimestampMixin):
    """Production country model"""
    
    __tablename__ = 'production_countries'
    
    iso_code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_country_association",
        back_populates="production_countries",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<ProductionCountry(iso_code='{self.iso_code}', name='{self.name}')>"


class SpokenLanguage(Base, TimestampMixin):
    """Spoken language model"""
    
    __tablename__ = 'spoken_languages'
    
    iso_code: Mapped[str] = mapped_column(String(2), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    english_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Relationships
    movies: Mapped[List["Movie"]] = relationship(
        "Movie",
        secondary="movie_language_association",
        back_populates="spoken_languages",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<SpokenLanguage(iso_code='{self.iso_code}', name='{self.name}')>"