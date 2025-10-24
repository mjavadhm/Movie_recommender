import asyncio
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from config import get_settings
from database import db_manager
from models import (
    Movie, Genre, Keyword, Person, ProductionCompany,
    ProductionCountry, SpokenLanguage, Provider, Video,
    MovieReleaseDate, Collection, MovieCastAssociation, MovieCrewAssociation
)

settings = get_settings()


class TMDbService:
    """سرویس مدیریت API های TMDb"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.TMDB_API_KEY
        if not self.api_key:
            raise ValueError("❌ TMDB_API_KEY تنظیم نشده است!")
        
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """بستن کلاینت HTTP"""
        await self.client.aclose()
    
    async def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """درخواست به API"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"❌ خطا در درخواست: {e}")
            return {}
    
    async def search_movie(self, query: str, language: str = "en-US") -> List[Dict]:
        """جستجوی فیلم"""
        print(f"🔍 در حال جستجوی: {query}")
        data = await self._request("search/movie", {
            "query": query,
            "language": language
        })
        return data.get('results', [])
    
    async def get_movie_details(self, movie_id: int, language: str = "en-US") -> Dict:
        """دریافت جزئیات کامل فیلم"""
        print(f"📥 دریافت اطلاعات فیلم ID: {movie_id}")
        return await self._request(
            f"movie/{movie_id}",
            {
                "language": language,
                "append_to_response": "credits,keywords,videos,release_dates,watch/providers"
            }
        )
    
    async def get_or_create_genre(self, session, genre_data: Dict) -> Genre:
        """دریافت یا ساخت ژانر"""
        result = await session.execute(
            select(Genre).where(Genre.tmdb_id == genre_data['id'])
        )
        genre = result.scalar_one_or_none()
        
        if not genre:
            genre = Genre(
                tmdb_id=genre_data['id'],
                name=genre_data['name']
            )
            session.add(genre)
            await session.flush()
        
        return genre
    
    async def get_or_create_keyword(self, session, keyword_data: Dict) -> Keyword:
        """دریافت یا ساخت کلیدواژه"""
        result = await session.execute(
            select(Keyword).where(Keyword.tmdb_id == keyword_data['id'])
        )
        keyword = result.scalar_one_or_none()
        
        if not keyword:
            keyword = Keyword(
                tmdb_id=keyword_data['id'],
                name=keyword_data['name']
            )
            session.add(keyword)
            await session.flush()
        
        return keyword
    
    async def get_or_create_person(self, session, person_data: Dict) -> Person:
        """دریافت یا ساخت شخص (بازیگر/کارگردان)"""
        result = await session.execute(
            select(Person).where(Person.tmdb_id == person_data['id'])
        )
        person = result.scalar_one_or_none()
        
        if not person:
            person = Person(
                tmdb_id=person_data['id'],
                name=person_data['name'],
                profile_path=person_data.get('profile_path'),
                gender=person_data.get('gender')
            )
            session.add(person)
            await session.flush()
        
        return person
    
    async def get_or_create_company(self, session, company_data: Dict) -> ProductionCompany:
        """دریافت یا ساخت شرکت تولیدی"""
        result = await session.execute(
            select(ProductionCompany).where(ProductionCompany.tmdb_id == company_data['id'])
        )
        company = result.scalar_one_or_none()
        
        if not company:
            company = ProductionCompany(
                tmdb_id=company_data['id'],
                name=company_data['name'],
                logo_path=company_data.get('logo_path'),
                origin_country=company_data.get('origin_country')
            )
            session.add(company)
            await session.flush()
        
        return company
    
    async def get_or_create_country(self, session, country_data: Dict) -> ProductionCountry:
        """دریافت یا ساخت کشور"""
        # FIXED: Changed iso_3166_1 to iso_code
        result = await session.execute(
            select(ProductionCountry).where(ProductionCountry.iso_code == country_data['iso_3166_1'])
        )
        country = result.scalar_one_or_none()
        
        if not country:
            country = ProductionCountry(
                iso_code=country_data['iso_3166_1'],
                name=country_data['name']
            )
            session.add(country)
            await session.flush()
        
        return country
    
    async def get_or_create_language(self, session, language_data: Dict) -> SpokenLanguage:
        """دریافت یا ساخت زبان"""
        # FIXED: Changed iso_639_1 to iso_code
        result = await session.execute(
            select(SpokenLanguage).where(SpokenLanguage.iso_code == language_data['iso_639_1'])
        )
        language = result.scalar_one_or_none()
        
        if not language:
            language = SpokenLanguage(
                iso_code=language_data['iso_639_1'],
                name=language_data['name'],
                english_name=language_data.get('english_name')
            )
            session.add(language)
            await session.flush()
        
        return language
    
    async def get_or_create_collection(self, session, collection_data: Dict) -> Collection:
        """دریافت یا ساخت مجموعه"""
        result = await session.execute(
            select(Collection).where(Collection.tmdb_id == collection_data['id'])
        )
        collection = result.scalar_one_or_none()
        
        if not collection:
            collection = Collection(
                tmdb_id=collection_data['id'],
                name=collection_data['name'],
                poster_path=collection_data.get('poster_path'),
                backdrop_path=collection_data.get('backdrop_path'),
                overview=collection_data.get('overview')
            )
            session.add(collection)
            await session.flush()
        
        return collection
    
    async def save_movie(self, movie_data: Dict) -> Optional[Movie]:
        """ذخیره کامل اطلاعات فیلم"""
        
        async with db_manager.get_session() as session:
            try:
                # چک کردن اینکه فیلم قبلاً وجود داره یا نه
                result = await session.execute(
                    select(Movie).where(Movie.tmdb_id == movie_data['id'])
                )
                existing_movie = result.scalar_one_or_none()
                
                if existing_movie:
                    print(f"⚠️  فیلم '{movie_data['title']}' قبلاً در دیتابیس وجود دارد")
                    return existing_movie
                
                print(f"💾 در حال ذخیره فیلم: {movie_data['title']}")
                
                # ساخت فیلم
                movie = Movie(
                    tmdb_id=movie_data['id'],
                    imdb_id=movie_data.get('imdb_id'),
                    title=movie_data['title'],
                    original_title=movie_data.get('original_title'),
                    original_language=movie_data.get('original_language'),
                    overview=movie_data.get('overview'),
                    tagline=movie_data.get('tagline'),
                    status=movie_data.get('status'),
                    release_date=datetime.strptime(movie_data['release_date'], '%Y-%m-%d').date() 
                        if movie_data.get('release_date') else None,
                    runtime=movie_data.get('runtime'),
                    budget=movie_data.get('budget', 0),
                    revenue=movie_data.get('revenue', 0),
                    popularity=movie_data.get('popularity', 0.0),
                    vote_average=movie_data.get('vote_average', 0.0),
                    vote_count=movie_data.get('vote_count', 0),
                    poster_path=movie_data.get('poster_path'),
                    backdrop_path=movie_data.get('backdrop_path'),
                    homepage=movie_data.get('homepage'),
                    adult=movie_data.get('adult', False)
                )
                
                # اضافه کردن Collection
                if movie_data.get('belongs_to_collection'):
                    collection = await self.get_or_create_collection(
                        session, 
                        movie_data['belongs_to_collection']
                    )
                    movie.collection_id = collection.id
                
                # اضافه کردن ژانرها
                if movie_data.get('genres'):
                    for genre_data in movie_data['genres']:
                        genre = await self.get_or_create_genre(session, genre_data)
                        movie.genres.append(genre)
                
                # اضافه کردن کلیدواژه‌ها
                if movie_data.get('keywords', {}).get('keywords'):
                    for keyword_data in movie_data['keywords']['keywords']:
                        keyword = await self.get_or_create_keyword(session, keyword_data)
                        movie.keywords.append(keyword)
                
                # اضافه کردن شرکت‌های تولیدی
                if movie_data.get('production_companies'):
                    for company_data in movie_data['production_companies']:
                        company = await self.get_or_create_company(session, company_data)
                        movie.production_companies.append(company)
                
                # اضافه کردن کشورها
                if movie_data.get('production_countries'):
                    for country_data in movie_data['production_countries']:
                        country = await self.get_or_create_country(session, country_data)
                        movie.production_countries.append(country)
                
                # اضافه کردن زبان‌ها
                if movie_data.get('spoken_languages'):
                    for language_data in movie_data['spoken_languages']:
                        language = await self.get_or_create_language(session, language_data)
                        movie.spoken_languages.append(language)
                
                # اضافه کردن بازیگران (Cast)
                if movie_data.get('credits', {}).get('cast'):
                    for cast_data in movie_data['credits']['cast'][:30]:  # 30 نفر اول
                        person = await self.get_or_create_person(session, cast_data)
                        association = MovieCastAssociation(
                            person_id=person.id,
                            character_name=cast_data.get('character'),
                            cast_order=cast_data.get('order'),
                            credit_id=cast_data.get('credit_id'),
                        )
                        movie.cast_associations.append(association)

                # اضافه کردن عوامل (Crew)
                if movie_data.get('credits', {}).get('crew'):
                    for crew_data in movie_data['credits']['crew'][:30]:  # 30 نفر اول
                        person = await self.get_or_create_person(session, crew_data)
                        association = MovieCrewAssociation(
                            person_id=person.id,
                            department=crew_data.get('department'),
                            job=crew_data.get('job'),
                            credit_id=crew_data.get('credit_id'),
                        )
                        movie.crew_associations.append(association)
                
                # اضافه کردن تاریخ‌های انتشار (Release Dates)
                if movie_data.get('release_dates', {}).get('results'):
                    for country_release in movie_data['release_dates']['results']:
                        for release in country_release['release_dates']:
                            release_date_str = release['release_date'].rstrip('Z')
                            release_date_obj = datetime.fromisoformat(release_date_str).date()

                            release_date = MovieReleaseDate(
                                movie=movie,
                                country_code=country_release['iso_3166_1'],
                                release_date=release_date_obj,
                                certification=release.get('certification'),
                                type=release.get('type')
                            )
                            session.add(release_date)

                # اضافه کردن ویدیوها (تریلرها)
                if movie_data.get('videos', {}).get('results'):
                    for video_data in movie_data['videos']['results']:
                        video = Video(
                            tmdb_video_id=video_data['id'],
                            key=video_data['key'],
                            site=video_data['site'],
                            type=video_data['type'],
                            name=video_data['name'],
                            size=video_data.get('size'),
                            official=video_data.get('official', False),
                            movie=movie
                        )
                        session.add(video)
                
                session.add(movie)
                await session.commit()
                await session.refresh(movie)
                
                print(f"✅ فیلم '{movie.title}' با موفقیت ذخیره شد!")
                return movie
                
            except Exception as e:
                await session.rollback()
                print(f"❌ خطا در ذخیره فیلم: {e}")
                import traceback
                traceback.print_exc()
                return None
    
    async def search_and_save_movie(self, query: str) -> Optional[Movie]:
        """جستجو و ذخیره فیلم"""
        # جستجوی فیلم
        results = await self.search_movie(query)
        
        if not results:
            print(f"❌ فیلمی با نام '{query}' پیدا نشد")
            return None
        
        # نمایش نتایج
        print(f"\n📋 {len(results)} فیلم پیدا شد:")
        for i, movie in enumerate(results[:5], 1):
            year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A'
            print(f"  {i}. {movie['title']} ({year}) - ID: {movie['id']}")
        
        # انتخاب اولین نتیجه
        selected_movie = results[0]
        movie_id = selected_movie['id']
        
        # دریافت جزئیات کامل
        movie_details = await self.get_movie_details(movie_id)
        
        if not movie_details:
            print("❌ خطا در دریافت جزئیات فیلم")
            return None
        
        # ذخیره فیلم
        return await self.save_movie(movie_details)


# تابع اصلی برای تست
async def main():
    """تست سرویس"""
    service = TMDbService()
    
    try:
        # مثال: ذخیره فیلم Inception
        movie = await service.search_and_save_movie("Inception")
        
        if movie:
            print(f"\n🎬 اطلاعات ذخیره شده:")
            print(f"  📌 عنوان: {movie.title}")
            print(f"  📅 سال: {movie.release_date}")
            print(f"  ⭐ امتیاز: {movie.vote_average}/10")
            print(f"  🎭 ژانرها: {', '.join([g.name for g in movie.genres])}")
    
    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(main())