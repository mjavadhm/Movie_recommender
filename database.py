from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .config import get_settings
from .models.base import Base


class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self):
        self.settings = get_settings()
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None
    
    def get_engine(self) -> AsyncEngine:
        """Get or create async engine"""
        if self._engine is None:
            self._engine = create_async_engine(
                self.settings.DATABASE_URL,
                echo=self.settings.DATABASE_ECHO,
                future=True,
                pool_size=self.settings.POOL_SIZE,
                max_overflow=self.settings.MAX_OVERFLOW,
                pool_timeout=self.settings.POOL_TIMEOUT,
                pool_recycle=self.settings.POOL_RECYCLE,
            )
        return self._engine
    
    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """Get or create session maker"""
        if self._sessionmaker is None:
            self._sessionmaker = async_sessionmaker(
                bind=self.get_engine(),
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
        return self._sessionmaker
    
    async def ping_database(self) -> bool:
        """Test database connectivity"""
        try:
            async with self.get_engine().connect() as conn:
                await conn.execute(text("SELECT 1"))
                print("✅ Successfully connected to the database!")
                return True
        except SQLAlchemyError as e:
            print(f"❌ Error connecting to database: {e}")
            return False
    
    async def create_tables(self) -> None:
        """Create all tables defined in models"""
        async with self.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully")
    
    async def drop_tables(self) -> None:
        """Drop all tables (use with caution!)"""
        async with self.get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("⚠️  All tables dropped")
    
    async def close(self) -> None:
        """Close database connections"""
        if self._engine:
            await self._engine.dispose()
            print("✅ Database connections closed")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session with automatic cleanup"""
        session_maker = self.get_sessionmaker()
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database manager instance
db_manager = DatabaseManager()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session"""
    async with db_manager.get_session() as session:
        yield session