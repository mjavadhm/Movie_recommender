"""
اسکریپت ساده برای اضافه کردن فیلم به دیتابیس
"""
import asyncio
import sys
from tmdb_service import TMDbService


async def add_movie(movie_name: str):
    """اضافه کردن یک فیلم به دیتابیس"""
    service = TMDbService()
    
    try:
        print(f"\n{'='*60}")
        print(f"🎬 جستجو و ذخیره فیلم: {movie_name}")
        print(f"{'='*60}\n")
        
        movie = await service.search_and_save_movie(movie_name)
        
        if movie:
            print(f"\n{'='*60}")
            print("✅ فیلم با موفقیت اضافه شد!")
            print(f"{'='*60}")
            print(f"\n📊 خلاصه اطلاعات:")
            print(f"  🎬 عنوان: {movie.title}")
            print(f"  📅 تاریخ انتشار: {movie.release_date}")
            print(f"  ⏱️  مدت زمان: {movie.runtime} دقیقه")
            print(f"  ⭐ امتیاز: {movie.vote_average}/10 ({movie.vote_count} رای)")
            print(f"  💰 بودجه: ${movie.budget:,}")
            print(f"  💵 درآمد: ${movie.revenue:,}")
            print(f"  🎭 ژانرها: {', '.join([g.name for g in movie.genres])}")
            if movie.overview:
                print(f"  📝 خلاصه: {movie.overview[:200]}...")
        else:
            print("\n❌ فیلم اضافه نشد!")
    
    finally:
        await service.close()


async def add_multiple_movies(movie_names: list):
    """اضافه کردن چند فیلم"""
    service = TMDbService()
    
    try:
        print(f"\n{'='*60}")
        print(f"🎬 اضافه کردن {len(movie_names)} فیلم به دیتابیس")
        print(f"{'='*60}\n")
        
        for i, movie_name in enumerate(movie_names, 1):
            print(f"\n[{i}/{len(movie_names)}] در حال پردازش: {movie_name}")
            print("-" * 60)
            
            movie = await service.search_and_save_movie(movie_name)
            
            if movie:
                print(f"✅ {movie.title} اضافه شد")
            else:
                print(f"❌ خطا در اضافه کردن {movie_name}")
            
            # تاخیر کوتاه برای رعایت rate limit API
            if i < len(movie_names):
                await asyncio.sleep(0.5)
        
        print(f"\n{'='*60}")
        print("✅ تمام شد!")
        print(f"{'='*60}")
    
    finally:
        await service.close()


def main():
    """تابع اصلی"""
    if len(sys.argv) < 2:
        print("استفاده:")
        print("  python add_movie.py \"نام فیلم\"")
        print("  python add_movie.py \"فیلم 1\" \"فیلم 2\" \"فیلم 3\"")
        print("\nمثال:")
        print("  python add_movie.py \"Inception\"")
        print("  python add_movie.py \"The Matrix\" \"Interstellar\" \"The Dark Knight\"")
        return
    
    movie_names = sys.argv[1:]
    
    if len(movie_names) == 1:
        asyncio.run(add_movie(movie_names[0]))
    else:
        asyncio.run(add_multiple_movies(movie_names))


if __name__ == "__main__":
    main()