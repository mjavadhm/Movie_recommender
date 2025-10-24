
from .base import Base, TimestampMixin

from .associations import (
    movie_genre_association,
    movie_keyword_association,
    movie_company_association,
    movie_country_association,
    movie_language_association,
    movie_provider_association,
    MovieCastAssociation,
    MovieCrewAssociation,
)

#  Models
from .movie import Movie
from .person import Person
from .user import User
from .genre import Genre
from .keyword import Keyword
from .collection import Collection
from .production import ProductionCompany, ProductionCountry, SpokenLanguage
from .provider import Provider
from .video import Video, MovieReleaseDate
from .ratings import UserMovieRating

__all__ = [
    # Base Classes
    "Base",
    "TimestampMixin",
    
    # Association Tables
    "movie_genre_association",
    "movie_keyword_association",
    "movie_company_association",
    "movie_country_association",
    "movie_language_association",
    "movie_provider_association",
    "MovieCastAssociation",
    "MovieCrewAssociation",
    
    # Main Models
    "Movie",
    "Person",
    "User",
    "Genre",
    "Keyword",
    "Collection",
    "ProductionCompany",
    "ProductionCountry",
    "SpokenLanguage",
    "Provider",
    "Video",
    "MovieReleaseDate",
    "UserMovieRating",
]