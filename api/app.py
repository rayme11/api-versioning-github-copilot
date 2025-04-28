from fastapi import FastAPI
from routers.hello_router import router as hello_router

app = FastAPI()

# Include the hello_router
app.include_router(hello_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)