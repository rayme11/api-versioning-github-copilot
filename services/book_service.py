from typing import List, Optional
from bson import ObjectId
from datetime import datetime, timezone
from docs.models.book import Book
from repositories.book_repository import BookRepository

class BookServiceError(Exception):
    """Base exception for BookService errors."""
    pass

class BookNotFoundError(BookServiceError):
    """Raised when a book is not found."""
    pass

class InvalidBookDataError(BookServiceError):
    """Raised when invalid book data is provided."""
    pass

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def create_book(self, book: Book) -> str:
        if not book.title or not book.author:
            raise InvalidBookDataError("Book must have a title and an author.")
        if book.price < 0:
            raise InvalidBookDataError("Book price cannot be negative.")
        try:
            return self.book_repository.create_book(book)
        except Exception as e:
            raise BookServiceError(f"Failed to create book: {e}")

    def get_book_by_id(self, book_id: str) -> Book:
        if not ObjectId.is_valid(book_id):
            raise InvalidBookDataError("Invalid book ID format.")
        book = self.book_repository.get_one_book(book_id)
        if not book:
            raise BookNotFoundError(f"Book with ID {book_id} not found.")
        return book

    def get_all_books(self) -> List[Book]:
        try:
            return self.book_repository.get_all_books()
        except Exception as e:
            raise BookServiceError(f"Failed to fetch books: {e}")

    def soft_delete_book(self, book_id: str) -> bool:
        if not ObjectId.is_valid(book_id):
            raise InvalidBookDataError("Invalid book ID format.")
        try:
            success = self.book_repository.soft_delete_book(book_id)
            if not success:
                raise BookNotFoundError(f"Book with ID {book_id} not found or already inactive.")
            return success
        except Exception as e:
            raise BookServiceError(f"Failed to delete book: {e}")
