from typing import Optional, List
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId
from datetime import datetime
from docs.models.book import Book
from pydantic import ValidationError

class BookRepository:
    def __init__(self, database_name: str, connection_string: str = "mongodb://localhost:27017"):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db["books"]

    def create_book(self, book: Book) -> str:
        if book is None:
            raise ValueError("Book cannot be None")  # Add validation for None
        try:
            book_data = book.dict()
            result = self.collection.insert_one(book_data)
            return str(result.inserted_id)
        except ValidationError as e:
            raise ValueError(f"Invalid book data: {e}")
        except PyMongoError as e:
            raise RuntimeError(f"Database error during book creation: {e}")

    def update_book(self, book_id: str, book: Book) -> bool:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": book.dict(exclude_unset=True), "$currentDate": {"updated_date": True}}
            )
            return result.modified_count > 0
        except ValidationError as e:
            raise ValueError(f"Invalid book data: {e}")
        except PyMongoError as e:
            raise RuntimeError(f"Database error during book update: {e}")

    def soft_delete_book(self, book_id: str) -> bool:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": {"status": "INACTIVE", "inactive_date": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            raise RuntimeError(f"Database error during book soft delete: {e}")

    def get_all_books(self) -> List[Book]:
        try:
            books = self.collection.find({"status": {"$ne": "INACTIVE"}})
            return [Book(**book, exclude_unset=True) for book in books]  # Handle missing fields
        except ValidationError as e:
            raise ValueError(f"Invalid book data retrieved from database: {e}")
        except PyMongoError as e:
            raise RuntimeError(f"Database error during fetching all books: {e}")

    def get_one_book(self, book_id: str) -> Optional[Book]:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")
        try:
            book = self.collection.find_one({"_id": ObjectId(book_id), "status": {"$ne": "INACTIVE"}})
            return Book(**book, exclude_unset=True) if book else None  # Handle missing fields
        except ValidationError as e:
            raise ValueError(f"Invalid book data retrieved from database: {e}")
        except PyMongoError as e:
            raise RuntimeError(f"Database error during fetching one book: {e}")
