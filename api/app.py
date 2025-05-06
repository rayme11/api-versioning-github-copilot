from fastapi import FastAPI
from .routers.hello_router import router as hello_router  # Use relative import

app = FastAPI()

# Include the hello_router
app.include_router(hello_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)  # Adjusted module path for uvicorn