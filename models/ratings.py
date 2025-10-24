from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Integer, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .movie import Movie


class UserMovieRating(Base, TimestampMixin):
    """User movie rating model (1-10 scale)"""
    
    __tablename__ = 'user_movie_ratings'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('movies.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="ratings")
    movie: Mapped["Movie"] = relationship("Movie", back_populates="user_ratings")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 10', name='rating_range_check'),
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),
    )
    
    def __repr__(self) -> str:
        return f"<UserMovieRating(user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating})>"