import asyncio
from database import db_manager


async def initialize_database():
    """Initialize the database"""
    print("🚀 Initializing database...")
    
    # Test connection
    connected = await db_manager.ping_database()
    if not connected:
        print("❌ Failed to connect to database. Check your DATABASE_URL in .env")
        return
    
    # Create all tables
    await db_manager.create_tables()
    
    print("✅ Database initialized successfully!")
    print("\\n📝 Next steps:")
    print("   1. Run the TMDb service to fetch movie data")
    print("   2. Add test users for the recommendation system")
    print("   3. Collect user ratings for training")


async def drop_and_recreate():
    """Drop all tables and recreate (WARNING: DESTRUCTIVE)"""
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() == 'yes':
        await db_manager.drop_tables()
        await db_manager.create_tables()
        print("✅ Database reset complete")
    else:
        print("❌ Operation cancelled")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        asyncio.run(drop_and_recreate())
    else:
        asyncio.run(initialize_database())