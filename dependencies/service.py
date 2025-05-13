from motor.motor_asyncio import AsyncIOMotorClient
from repositories.book_repository import BookRepository
from services.book_service import BookService
from config import MONGO_URI, DATABASE_NAME

async def get_database():
    client = AsyncIOMotorClient(MONGO_URI)
    return client[DATABASE_NAME]

async def get_book_repository():
    db = await get_database()
    return BookRepository(db)

async def get_book_service():
    repository = await get_book_repository()
    return BookService(repository)

