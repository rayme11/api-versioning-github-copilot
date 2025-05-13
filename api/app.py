from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.routers.hello_router import router as hello_router
from api.routers.books_router import router as books_router
from services.book_service import BookNotFoundError, InvalidBookDataError

app = FastAPI()

@app.exception_handler(InvalidBookDataError)
async def invalid_book_data_handler(request: Request, exc: InvalidBookDataError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(BookNotFoundError)
async def book_not_found_handler(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

# Include routers
app.include_router(hello_router)
app.include_router(books_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)