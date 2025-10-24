from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .ratings import UserMovieRating


class User(Base, TimestampMixin):
    """User model for test users"""
    
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    ratings: Mapped[List["UserMovieRating"]] = relationship(
        "UserMovieRating",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"