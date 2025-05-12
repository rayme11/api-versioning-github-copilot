from fastapi import APIRouter, Depends, HTTPException  # Added APIRouter import
from typing import List
from bson import ObjectId
from docs.models.book import Book
from services.book_service import BookService, BookNotFoundError, InvalidBookDataError
from dependencies.service import get_book_service

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=str)
async def create_book(book: Book, book_service: BookService = Depends(get_book_service)):
    """
    Create a new book.
    """
    try:
        return await book_service.create_book(book)
    except InvalidBookDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create book.")

@router.get("/", response_model=List[Book])
async def get_books(book_service: BookService = Depends(get_book_service)):
    """
    Retrieve all books.
    """
    try:
        return await book_service.get_all_books()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch books.")

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: str, book_service: BookService = Depends(get_book_service)):
    """
    Retrieve a book by its ID.
    """
    try:
        return await book_service.get_book_by_id(book_id)
    except InvalidBookDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch book.")

@router.put("/{book_id}", response_model=bool)
async def update_book(book_id: str, book: Book, book_service: BookService = Depends(get_book_service)):
    """
    Update a book by its ID.
    """
    try:
        return await book_service.update_book(book_id, book)
    except InvalidBookDataError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update book.")
