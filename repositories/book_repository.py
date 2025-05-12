from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone
from docs.models.book import Book
from pydantic import ValidationError

class BookRepository:
    def __init__(self, client: AsyncIOMotorClient, database_name: str):
        self.client = client
        self.db = self.client[database_name]
        self.collection = self.db["books"]

    async def create_book(self, book: Book) -> str:
        if book is None:
            raise ValueError("Book cannot be None")
        try:
            book_data = book.model_dump()  # Updated from dict to model_dump
            result = await self.collection.insert_one(book_data)
            return str(result.inserted_id)
        except ValidationError as e:
            raise ValueError(f"Invalid book data: {e}")
        except Exception as e:
            raise RuntimeError(f"Database error during book creation: {e}")

    async def update_book(self, book_id: str, book: Book) -> bool:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": book.model_dump(exclude_unset=True), "$currentDate": {"updated_date": True}}
            )
            return result.modified_count > 0
        except ValidationError as e:
            raise ValueError(f"Invalid book data: {e}")
        except Exception as e:
            raise RuntimeError(f"Database error during book update: {e}")

    async def soft_delete_book(self, book_id: str) -> bool:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": {"status": "INACTIVE", "inactive_date": datetime.now(timezone.utc)}}
            )
            return result.modified_count > 0
        except Exception as e:
            raise RuntimeError(f"Database error during book soft delete: {e}")

    async def get_all_books(self) -> List[Book]:
        try:
            books_cursor = self.collection.find({"status": {"$ne": "INACTIVE"}})
            books = []
            async for book in books_cursor:
                books.append(Book(**book))
            return books
        except ValidationError as e:
            raise ValueError(f"Invalid book data retrieved from database: {e}")
        except Exception as e:
            raise RuntimeError(f"Database error during fetching all books: {e}")

    async def get_one_book(self, book_id: str) -> Optional[Book]:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")
        try:
            book = await self.collection.find_one({"_id": ObjectId(book_id), "status": {"$ne": "INACTIVE"}})
            return Book(**book) if book else None
        except ValidationError as e:
            raise ValueError(f"Invalid book data retrieved from database: {e}")
        except Exception as e:
            raise RuntimeError(f"Database error during fetching one book: {e}")
