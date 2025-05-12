from motor.motor_asyncio import AsyncIOMotorClient
from repositories.book_repository import BookRepository
from services.book_service import BookService
from config import MONGO_URI, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URI)
book_repository = BookRepository(client, DATABASE_NAME)

def get_book_repository() -> BookRepository:
    return book_repository

def get_book_service() -> BookService:
    return BookService(book_repository)

