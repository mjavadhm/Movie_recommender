
class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    tmdb_id = Column(String(100), unique=True, nullable=False) 
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"))
    key = Column(String(100)) 
    name = Column(String(255))
    site = Column(String(50)) 
    type = Column(String(50)) 
    movie = relationship("Movie", back_populates="videos")


class MovieReleaseDate(Base):
    __tablename__ = 'movie_release_dates'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"))
    country_iso = Column(String(10), primary_key=True)
    release_date = Column(Date)
    certification = Column(String(20)) 
    type = Column(Integer) 
    movie = relationship("Movie", back_populates="release_dates")


class Provider(Base):
    __tablename__ = 'providers'
    id = Column(Integer, primary_key=True)
    tmdb_provider_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    logo_path = Column(String(255))

class MovieWatchProvider(Base):
    __tablename__ = 'movie_watch_providers'
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete="CASCADE"))
    provider_id = Column(Integer, ForeignKey('providers.id', ondelete="CASCADE"))
    country_iso = Column(String(10), nullable=False, primary_key=True)
    type = Column(String(20), nullable=False, primary_key=True) 
    
    movie = relationship("Movie", back_populates="watch_providers")
    provider = relationship("Provider")