from pydantic import BaseModel, Field, constr
from typing import List, Dict, Optional
from datetime import datetime

class Book(BaseModel):
    title: constr(strip_whitespace=True, min_length=1) = Field(..., description="The title of the book")
    author: constr(strip_whitespace=True, min_length=1) = Field(..., description="The author of the book")
    description: Optional[str] = Field(None, description="A brief description of the book")
    language: constr(strip_whitespace=True, min_length=1) = Field(..., description="The language of the book")
    publisher: Optional[str] = Field(None, description="The publisher of the book")
    publisher_date: Optional[datetime] = Field(None, description="The publication date of the book")
    isbn: constr(regex=r"^\d{10}(\d{3})?$") = Field(..., description="The ISBN of the book")
    price: float = Field(..., ge=0, description="The price of the book")
    status: constr(strip_whitespace=True, regex=r"^(PENDING|ACTIVE|INACTIVE)$") = Field(..., description="The status of the book")
    created_date: datetime = Field(default_factory=datetime.utcnow, description="The date the book was created")
    updated_date: Optional[datetime] = Field(None, description="The date the book was last updated")
    inactive_date: Optional[datetime] = Field(None, description="The date the book was marked as inactive")
    ratings_by_stars: Optional[Dict[int, int]] = Field(default_factory=dict, description="Ratings by stars (e.g., {1: 10, 2: 20})")
    number_of_reviews: int = Field(default=0, ge=0, description="The number of reviews for the book")

    class model_config:  # Renamed from ModelConfig to model_config
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A novel set in the Jazz Age that explores themes of wealth, love, and the American Dream.",
                "language": "English",
                "publisher": "Scribner",
                "publisher_date": "1925-04-10T00:00:00",
                "isbn": "9780743273565",
                "price": 10.99,
                "status": "ACTIVE",
                "created_date": "2023-10-01T12:00:00",
                "updated_date": "2023-10-10T12:00:00",
                "inactive_date": None,
                "ratings_by_stars": {1: 5, 2: 10, 3: 15, 4: 20, 5: 50},
                "number_of_reviews": 100,
            }
        }
