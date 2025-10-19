from sqlalchemy import Table, Column, Integer, String, ForeignKey
from . import Base

movie_genre_association = Table('movie_genre_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

movie_keyword_association = Table('movie_keyword_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('keyword_id', Integer, ForeignKey('keywords.id', ondelete="CASCADE"), primary_key=True)
)

movie_company_association = Table('movie_company_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('company_id', Integer, ForeignKey('production_companies.id', ondelete="CASCADE"), primary_key=True)
)

movie_country_association = Table('movie_country_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('country_iso', String, ForeignKey('production_countries.iso_3166_1', ondelete="CASCADE"), primary_key=True)
)

movie_language_association = Table('movie_language_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('language_iso', String, ForeignKey('spoken_languages.iso_639_1', ondelete="CASCADE"), primary_key=True)
)