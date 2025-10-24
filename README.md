# Movie Data Warehouse & Recommendation Engine

## Overview
A comprehensive data warehouse for movie information built with SQLAlchemy async and PostgreSQL. This serves as the foundation for a movie recommendation engine based on content analysis and user ratings.

## Features
- ✅ Fully normalized database schema
- ✅ Async SQLAlchemy with connection pooling
- ✅ Type-safe models with Python type hints
- ✅ Support for TMDb API integration
- ✅ Many-to-many relationships for genres, keywords, cast, crew, etc.
- ✅ User rating system (1-10 scale)
- ✅ Video/trailer management
- ✅ Watch provider tracking (Netflix, Disney+, etc.)
- ✅ Release date tracking per country

## Tech Stack
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0+ (Async)
- **Database**: PostgreSQL
- **Drivers**: asyncpg, psycopg2-binary
- **APIs**: TMDb API

## Project Structure
```
movie_warehouse/
├── __init__.py
├── config.py                  # Database & API configuration
├── database.py                # Database engine and session management
├── models/
│   ├── __init__.py
│   ├── base.py               # Base model with timestamps
│   ├── movie.py              # Main Movie model
│   ├── person.py             # Person (cast/crew) model
│   ├── user.py               # User model
│   ├── genre.py              # Genre model
│   ├── keyword.py            # Keyword model
│   ├── production.py         # Production companies, countries, languages
│   ├── collection.py         # Collection model
│   ├── provider.py           # Watch provider model
│   ├── video.py              # Video/trailer model + release dates
│   ├── associations.py       # M2M association tables
│   └── ratings.py            # User rating model
├── services/
│   ├── __init__.py
│   └── tmdb_service.py       # TMDb API integration
└── alembic/                  # Database migrations
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/movie_warehouse
DATABASE_ECHO=True
TMDB_API_KEY=your_tmdb_api_key_here
```

### 3. Initialize Database
```python
import asyncio
from movie_warehouse.database import db_manager

async def init_db():
    await db_manager.ping_database()
    await db_manager.create_tables()

asyncio.run(init_db())
```

## Database Schema

### Main Tables
- **movies** - Core movie information
- **persons** - Cast and crew members
- **users** - Test users for recommendation system

### Reference Tables
- **genres** - Movie genres (Action, Drama, etc.)
- **keywords** - Movie keywords/tags
- **collections** - Movie collections (MCU, Star Wars, etc.)
- **production_companies** - Production companies
- **production_countries** - Countries
- **spoken_languages** - Languages
- **providers** - Streaming providers (Netflix, Disney+, etc.)

### Association Tables (Many-to-Many)
- **movie_genre_association**
- **movie_keyword_association**
- **movie_company_association**
- **movie_country_association**
- **movie_language_association**
- **movie_provider_association**
- **movie_cast_association** (includes character name, order)
- **movie_crew_association** (includes department, job)

### Detail Tables (One-to-Many)
- **videos** - Trailers and clips
- **movie_release_dates** - Release dates per country
- **user_movie_ratings** - User ratings (1-10 scale)

## Usage Example

```python
import asyncio
from sqlalchemy import select
from movie_warehouse.database import db_manager
from movie_warehouse.models import Movie, Genre, Person

async def example_queries():
    async with db_manager.get_session() as session:
        # Get all action movies
        result = await session.execute(
            select(Movie)
            .join(Movie.genres)
            .where(Genre.name == "Action")
            .limit(10)
        )
        action_movies = result.scalars().all()
        
        # Get movie with all relationships loaded
        movie = await session.get(Movie, 1)
        print(f"Title: {movie.title}")
        print(f"Genres: {[g.name for g in movie.genres]}")
        print(f"Cast: {[p.name for p in movie.cast[:5]]}")

asyncio.run(example_queries())
```

## Database Migrations with Alembic

### Initialize Alembic
```bash
alembic init alembic
```

### Generate Migration
```bash
alembic revision --autogenerate -m "Initial migration"
```

### Apply Migration
```bash
alembic upgrade head
```

## Next Steps
1. ✅ Implement TMDb API service for data fetching
2. ✅ Create ETL pipeline for automated data updates
3. ✅ Build recommendation engine (content-based + collaborative filtering)
4. ✅ Add data validation and error handling
5. ✅ Implement caching layer (Redis)
6. ✅ Create REST API for data access

## License
MIT