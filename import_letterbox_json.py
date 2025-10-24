import asyncio
import json
import sys
from typing import List, Dict, Optional
from pathlib import Path
from tmdb_service import TMDbService
from database import db_manager
from models import Movie, User, UserMovieRating
from sqlalchemy import select


class LetterboxdImporter:
    """Import movies from Letterboxd JSON export"""
    
    def __init__(self, username: str = "letterboxd_user"):
        self.service = TMDbService()
        self.username = username
        self.user = None
        
        # Statistics
        self.stats = {
            "total": 0,
            "imported": 0,
            "skipped": 0,
            "errors": 0,
            "ratings_added": 0,
        }
    
    async def close(self):
        """Close connections"""
        await self.service.close()
    
    async def get_or_create_user(self) -> User:
        """Get or create user for ratings"""
        async with db_manager.get_session() as session:
            result = await session.execute(
                select(User).where(User.username == self.username)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                user = User(
                    username=self.username,
                    full_name=f"Letterboxd User: {self.username}"
                )
                session.add(user)
                await session.commit()
                await session.refresh(user)
                print(f"✅ کاربر '{self.username}' ساخته شد")
            
            return user
    
    def parse_title_year(self, title_year: str) -> tuple[str, Optional[int]]:
        """
        Parse title and year from format: "Movie Title (2020)"
        Returns: (title, year)
        """
        if '(' in title_year and title_year.endswith(')'):
            title = title_year[:title_year.rindex('(')].strip()
            year_str = title_year[title_year.rindex('(')+1:-1].strip()
            try:
                year = int(year_str)
                return title, year
            except ValueError:
                return title_year, None
        return title_year, None
    
    async def find_best_match(self, title: str, year: Optional[int]) -> Optional[Dict]:
        """
        Find best matching movie from TMDb considering year
        """
        # Search for the movie
        results = await self.service.search_movie(title)
        
        if not results:
            return None
        
        # If we have a year, try to find exact match
        if year:
            for movie in results:
                movie_year = None
                if movie.get('release_date'):
                    try:
                        movie_year = int(movie['release_date'][:4])
                    except (ValueError, IndexError):
                        continue
                
                # Exact year match
                if movie_year == year:
                    return movie
            
            # If no exact match, try ±1 year tolerance
            for movie in results:
                movie_year = None
                if movie.get('release_date'):
                    try:
                        movie_year = int(movie['release_date'][:4])
                    except (ValueError, IndexError):
                        continue
                
                if movie_year and abs(movie_year - year) <= 1:
                    print(f"  ⚠️  استفاده از فیلم با سال نزدیک: {movie['title']} ({movie_year}) به جای ({year})")
                    return movie
        
        # No year match, return first result (most popular)
        if results:
            movie = results[0]
            movie_year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A'
            if year:
                print(f"  ⚠️  فیلم با سال مطابق پیدا نشد. استفاده از: {movie['title']} ({movie_year})")
            return movie
        
        return None
    
    async def add_rating(self, movie: Movie, rating: float, liked: bool):
        """Add user rating for a movie"""
        if not self.user:
            self.user = await self.get_or_create_user()
        
        async with db_manager.get_session() as session:
            try:
                # Check if rating already exists
                result = await session.execute(
                    select(UserMovieRating).where(
                        UserMovieRating.user_id == self.user.id,
                        UserMovieRating.movie_id == movie.id
                    )
                )
                existing_rating = result.scalar_one_or_none()
                
                if existing_rating:
                    # Update existing rating
                    existing_rating.rating = int(rating * 2)  # Convert 5-star to 10-point scale
                    print(f"  📝 رتبه‌بندی به‌روز شد: {rating} ستاره")
                else:
                    # Create new rating
                    user_rating = UserMovieRating(
                        user_id=self.user.id,
                        movie_id=movie.id,
                        rating=int(rating * 2)  # Convert 5-star to 10-point scale
                    )
                    session.add(user_rating)
                    self.stats["ratings_added"] += 1
                    print(f"  ⭐ رتبه‌بندی اضافه شد: {rating} ستاره → {int(rating * 2)}/10")
                
                await session.commit()
                
            except Exception as e:
                print(f"  ❌ خطا در ثبت رتبه‌بندی: {e}")
    
    async def import_movie(self, entry: Dict) -> bool:
        """Import a single movie from Letterboxd entry"""
        title_year = entry.get('title_year', '')
        rating = entry.get('user_rating')
        liked = entry.get('user_liked', False)
        
        title, year = self.parse_title_year(title_year)
        
        print(f"\n{'='*70}")
        print(f"🎬 {title} ({year if year else 'N/A'})")
        print(f"{'='*70}")
        
        try:
            # Find best match
            movie_data = await self.find_best_match(title, year)
            
            if not movie_data:
                print(f"  ❌ فیلم پیدا نشد در TMDb")
                self.stats["errors"] += 1
                return False
            
            # Check if already in database
            async with db_manager.get_session() as session:
                result = await session.execute(
                    select(Movie).where(Movie.tmdb_id == movie_data['id'])
                )
                existing_movie = result.scalar_one_or_none()
            
            if existing_movie:
                print(f"  ✓ فیلم از قبل در دیتابیس است")
                movie = existing_movie
                self.stats["skipped"] += 1
            else:
                # Get full details and save
                print(f"  📥 دریافت اطلاعات کامل...")
                movie_details = await self.service.get_movie_details(movie_data['id'])
                
                if not movie_details:
                    print(f"  ❌ خطا در دریافت جزئیات")
                    self.stats["errors"] += 1
                    return False
                
                movie = await self.service.save_movie(movie_details)
                
                if not movie:
                    print(f"  ❌ خطا در ذخیره فیلم")
                    self.stats["errors"] += 1
                    return False
                
                self.stats["imported"] += 1
            
            # Add rating if exists
            if rating and rating > 0:
                await self.add_rating(movie, rating, liked)
            
            return True
            
        except Exception as e:
            print(f"  ❌ خطا: {e}")
            self.stats["errors"] += 1
            import traceback
            traceback.print_exc()
            return False
    
    async def import_from_json(self, json_path: str):
        """Import all movies from JSON file"""
        print(f"\n{'='*70}")
        print(f"📂 خواندن فایل: {json_path}")
        print(f"{'='*70}\n")
        
        # Read JSON file
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ خطا در خواندن فایل: {e}")
            return
        
        if not isinstance(data, list):
            print("❌ فرمت فایل نادرست است. باید یک آرایه JSON باشد")
            return
        
        self.stats["total"] = len(data)
        print(f"📊 تعداد فیلم‌ها: {self.stats['total']}\n")
        
        # Get or create user for ratings
        self.user = await self.get_or_create_user()
        
        # Import each movie
        for i, entry in enumerate(data, 1):
            print(f"\n[{i}/{self.stats['total']}] ", end="")
            await self.import_movie(entry)
            
            # Small delay to respect API rate limits
            if i < self.stats['total']:
                await asyncio.sleep(0.3)
        
        # Print final statistics
        self.print_statistics()
    
    def print_statistics(self):
        """Print import statistics"""
        print(f"\n{'='*70}")
        print("📊 خلاصه نتایج Import")
        print(f"{'='*70}")
        print(f"  📝 کل فیلم‌ها:           {self.stats['total']}")
        print(f"  ✅ فیلم‌های جدید:        {self.stats['imported']}")
        print(f"  ⏭️  فیلم‌های تکراری:     {self.stats['skipped']}")
        print(f"  ❌ خطاها:               {self.stats['errors']}")
        print(f"  ⭐ رتبه‌بندی‌های ثبت شده: {self.stats['ratings_added']}")
        print(f"{'='*70}\n")


async def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("استفاده:")
        print("  python3 import_letterboxd.py <path_to_json> [username]")
        print("\nمثال:")
        print("  python3 import_letterboxd.py letterboxd_export.json")
        print("  python3 import_letterboxd.py letterboxd_export.json javad")
        return
    
    json_path = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else "letterboxd_user"
    
    if not Path(json_path).exists():
        print(f"❌ فایل پیدا نشد: {json_path}")
        return
    
    importer = LetterboxdImporter(username=username)
    
    try:
        await importer.import_from_json(json_path)
    finally:
        await importer.close()


if __name__ == "__main__":
    asyncio.run(main())