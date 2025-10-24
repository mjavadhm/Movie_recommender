from sqlalchemy import Table, Column, Integer, ForeignKey, String

from .base import Base


# Movie <-> Genre
movie_genre_association = Table(
    'movie_genre_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
)

# Movie <-> Keyword
movie_keyword_association = Table(
    'movie_keyword_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keywords.id', ondelete='CASCADE'), primary_key=True),
)

# Movie <-> Production Company
movie_company_association = Table(
    'movie_company_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('company_id', Integer, ForeignKey('production_companies.id', ondelete='CASCADE'), primary_key=True),
)

# Movie <-> Production Country
movie_country_association = Table(
    'movie_country_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('country_code', String(2), ForeignKey('production_countries.iso_code', ondelete='CASCADE'), primary_key=True),
)

# Movie <-> Spoken Language
movie_language_association = Table(
    'movie_language_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('language_code', String(2), ForeignKey('spoken_languages.iso_code', ondelete='CASCADE'), primary_key=True),
)

# Movie <-> Provider
movie_provider_association = Table(
    'movie_provider_association',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('provider_id', Integer, ForeignKey('providers.id', ondelete='CASCADE'), primary_key=True),
    Column('country_code', String(2), nullable=False),
    Column('type', String(20), nullable=False),  # 'flatrate', 'rent', 'buy'
)

# Movie <-> Cast (Person)
movie_cast_association = Table(
    'movie_cast_association',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False),
    Column('person_id', Integer, ForeignKey('persons.id', ondelete='CASCADE'), nullable=False),
    Column('character_name', String(255), nullable=True),
    Column('cast_order', Integer, nullable=True),
    Column('credit_id', String(50), nullable=True),
)

# Movie <-> Crew (Person)
movie_crew_association = Table(
    'movie_crew_association',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False),
    Column('person_id', Integer, ForeignKey('persons.id', ondelete='CASCADE'), nullable=False),
    Column('department', String(100), nullable=True),
    Column('job', String(100), nullable=True),
    Column('credit_id', String(50), nullable=True),
)