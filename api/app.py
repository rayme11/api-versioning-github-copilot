from fastapi import FastAPI
from api.routers.hello_router import router as hello_router  # Use absolute import
from api.routers.books_router import router as books_router  # Import books_router

app = FastAPI()

# Include the hello_router
app.include_router(hello_router)

# Include the books_router
app.include_router(books_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)