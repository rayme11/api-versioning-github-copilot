import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from docs.models.book import Book
from services.book_service import BookService, BookNotFoundError, InvalidBookDataError
from dependencies.service import get_book_service
from api.app import app

@pytest.fixture
def example_book():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "description": "Test Description",
        "language": "English",
        "publisher": "Test Publisher",
        "publisher_date": None,
        "isbn": "1234567890123",
        "price": 29.99,
        "status": "ACTIVE"
    }

@pytest.fixture
def mock_book_service(example_book):
    service = AsyncMock()
    
    # Mock create
    async def mock_create(*args, **kwargs):
        return "mocked_id"
    service.create_book.side_effect = mock_create
    
    # Mock get all
    async def mock_get_all(*args, **kwargs):
        return [Book(**example_book)]
    service.get_all_books.side_effect = mock_get_all
    
    # Mock get one
    async def mock_get_one(*args, **kwargs):
        return Book(**example_book)
    service.get_book_by_id.side_effect = mock_get_one
    
    # Mock update
    async def mock_update(*args, **kwargs):
        return True
    service.update_book.side_effect = mock_update
    
    # Mock delete
    async def mock_delete(*args, **kwargs):
        return True
    service.soft_delete_book.side_effect = mock_delete
    
    return service

@pytest.fixture
def client(mock_book_service):
    app.dependency_overrides[get_book_service] = lambda: mock_book_service
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_book(client):
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "1234567890123",
            "price": 29.99,
            "status": "ACTIVE"
        }
    )
    assert response.status_code == 200
    assert response.json() == "mocked_id"

def test_get_all_books_success(client, mock_book_service, example_book):
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == example_book["title"]

def test_get_book_by_id_success(client, mock_book_service, example_book):
    response = client.get("/books/mocked_id")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == example_book["title"]

def test_get_book_by_id_not_found(client, mock_book_service):
    async def mock_not_found(*args, **kwargs):
        raise BookNotFoundError("Book not found")
    mock_book_service.get_book_by_id.side_effect = mock_not_found
    
    response = client.get("/books/mocked_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_book_success(client, mock_book_service, example_book):
    response = client.put(
        "/books/mocked_id",
        json=example_book
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True

def test_update_book_not_found(client, mock_book_service, example_book):
    async def mock_not_found(*args, **kwargs):
        raise BookNotFoundError("Book not found")
    mock_book_service.update_book.side_effect = mock_not_found
    
    response = client.put(
        "/books/mocked_id",
        json=example_book
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_book_invalid_data(client, mock_book_service, example_book):
    async def mock_invalid(*args, **kwargs):
        raise InvalidBookDataError("Invalid data")
    mock_book_service.update_book.side_effect = mock_invalid
    
    response = client.put(
        "/books/mocked_id",
        json=example_book
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_delete_book_success(client, mock_book_service):
    response = client.delete("/books/mocked_id")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is True

def test_delete_book_not_found(client, mock_book_service):
    async def mock_not_found(*args, **kwargs):
        raise BookNotFoundError("Book not found")
    mock_book_service.soft_delete_book.side_effect = mock_not_found
    
    response = client.delete("/books/mocked_id")
    assert response.status_code == status.HTTP_404_NOT_FOUND