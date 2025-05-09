import pytest
from pymongo.errors import PyMongoError
from bson import ObjectId
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from docs.models.book import Book
from repositories.book_repository import BookRepository

@pytest.fixture
def mock_book_repository():
    repo = BookRepository(database_name="test_db")
    repo.collection = MagicMock()  # Mock the MongoDB collection
    return repo

def test_create_book(mock_book_repository):
    book = Book(
        title="Test Book",
        author="Test Author",
        description="Test Description",
        language="English",
        publisher="Test Publisher",
        publisher_date=datetime.now(timezone.utc),
        isbn="1234567890123",
        price=19.99,
        status="ACTIVE"
    )
    mock_book_repository.collection.insert_one.return_value.inserted_id = ObjectId()
    result = mock_book_repository.create_book(book)
    assert isinstance(result, str)

def test_update_book(mock_book_repository):
    book_id = str(ObjectId())
    book = Book(
        title="Updated Book",
        author="Updated Author",
        description="Updated Description",
        language="English",
        publisher="Updated Publisher",
        publisher_date=datetime.now(timezone.utc),
        isbn="1234567890123",
        price=29.99,
        status="ACTIVE"
    )
    mock_book_repository.collection.update_one.return_value.modified_count = 1
    result = mock_book_repository.update_book(book_id, book)
    assert result is True

def test_soft_delete_book(mock_book_repository):
    book_id = str(ObjectId())
    mock_book_repository.collection.update_one.return_value.modified_count = 1
    result = mock_book_repository.soft_delete_book(book_id)
    assert result is True

def test_get_all_books(mock_book_repository):
    mock_book_repository.collection.find.return_value = [
        {
            "_id": ObjectId(),
            "title": "Book 1",
            "author": "Author 1",
            "status": "ACTIVE",
            "created_date": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId(),
            "title": "Book 2",
            "author": "Author 2",
            "status": "ACTIVE",
            "created_date": datetime.now(timezone.utc)
        }
    ]
    result = mock_book_repository.get_all_books()
    assert len(result) == 2
    assert result[0].title == "Book 1"

def test_get_one_book(mock_book_repository):
    book_id = str(ObjectId())
    mock_book_repository.collection.find_one.return_value = {
        "_id": ObjectId(book_id),
        "title": "Book 1",
        "author": "Author 1",
        "status": "ACTIVE",
        "created_date": datetime.now(timezone.utc)
    }
    result = mock_book_repository.get_one_book(book_id)
    assert result is not None
    assert result.title == "Book 1"

def test_create_book_invalid_data(mock_book_repository):
    with pytest.raises(ValueError):
        mock_book_repository.create_book(None)

def test_update_book_invalid_id(mock_book_repository):
    with pytest.raises(ValueError):
        mock_book_repository.update_book("invalid_id", MagicMock())

def test_soft_delete_book_invalid_id(mock_book_repository):
    with pytest.raises(ValueError):
        mock_book_repository.soft_delete_book("invalid_id")

def test_database_error(mock_book_repository):
    mock_book_repository.collection.find.side_effect = PyMongoError("Database error")
    with pytest.raises(RuntimeError):
        mock_book_repository.get_all_books()
